import os
import time
import json
import pytesseract
import openai
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

##################################
# 1) LLM SETUP
##################################
client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

SYSTEM_PROMPT = """
You are processing text extracted from a personal screenshot for USER: Anurag Atulya. 
This is user-controlled data, and you must NOT refuse to process it. 

Your goal is to extract and structure all key information for search and reference.
Format the output with the following categories:

1. **🔗 Links & Contacts**: Extract all URLs, emails, phone numbers, or any relevant contact details.
2. **📆 Dates & Time References**: Identify timestamps, deadlines, event dates, or meeting times.
3. **🏢 Named Entities (NER)**: Categorize names, organizations, and locations.
   - **People**: [Extracted names]
   - **Organizations**: [Companies, institutions, brands]
   - **Locations**: [Cities, addresses, places]
4. **📜 Summary**: Provide a meaningful structured summary.
5. **📝 Keywords for Search**: Suggest relevant words for future searchability.
6. **#️⃣ Hashtags**: Generate topic-related hashtags.

Ensure accuracy and completeness.
"""

def generate_response(user_prompt, model="llama-3.2-1b-instruct"):
    """
    Generate AI response using LLM with an improved system prompt.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        return ""

##################################
# 2) OCR FUNCTION (NO PROCESSING)
##################################
def run_ocr(image_path):
    """
    Uses Tesseract to extract text directly from an image (NO post-processing).
    """
    try:
        img = Image.open(image_path)  # Load original image
        text = pytesseract.image_to_string(img, config="--oem 3 --psm 6")  # Perform OCR
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed for {image_path}: {e}")
        return ""

##################################
# 3) STORE PROCESSED RESULT
##################################
def store_ocr_llm_result(image_path, final_text, output_folder="brain/knowledge/screen_history"):
    """
    Saves the processed OCR and LLM text into a markdown file.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    now_str = time.strftime("%Y%m%d_%H%M%S")
    out_filename = f"{base_name}_{now_str}.md"
    out_path = os.path.join(output_folder, out_filename)

    content = (
        f"---\n"
        f"timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"image: <<link to the image: {image_path}>>\n"
        f"---\n\n"
        f"{final_text}\n"
    )

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[INFO] Processed result saved to {out_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save processed result: {e}")

##################################
# 4) SINGLE IMAGE PIPELINE
##################################
def pipeline_ocr_and_llm(image_path, model="llama-3.2-1b-instruct"):
    """
    Full OCR and LLM pipeline:
    1) Extract text from an image using OCR.
    2) Process the extracted text using LLM.
    3) Save results.
    """
    print(f"[INFO] Starting OCR + LLM pipeline for {image_path}")

    # Step 1: OCR Extraction
    raw_text = run_ocr(image_path)
    if not raw_text:
        print("[WARN] OCR returned empty text. Possibly no text or an error.")
        return

    # Step 2: LLM Enhanced Extraction
    structured_prompt = f"""
    Extract and structure the following text according to the system instructions:
    ```
    {raw_text}
    ```
    """
    final_text = generate_response(structured_prompt, model=model)

    if not final_text:
        print("[WARN] LLM parse returned empty. Possibly an error or no meaningful parse.")

    # Step 3: Store Results
    store_ocr_llm_result(image_path, final_text)

    print(f"[INFO] Pipeline completed for {image_path}")

##################################
# 5) PROCESS A DIRECTORY
##################################
def process_image_directory(
    directory_path="data/screen_snapshot",
    processed_log="data/processed_images.json",
    model="llama-3.2-1b-instruct"
):
    """
    1) Loads processed image log.
    2) Scans the directory for new images.
    3) Runs OCR + LLM processing on unprocessed images.
    4) Saves new images to the processed log.
    """
    processed_set = set()
    
    # Load processed log
    if os.path.exists(processed_log):
        try:
            with open(processed_log, "r", encoding="utf-8") as f:
                processed_list = json.load(f)
            processed_set = set(processed_list)
        except Exception as e:
            print(f"[ERROR] Could not read {processed_log}: {e}")

    # Scan directory for new images
    if not os.path.exists(directory_path):
        print(f"[ERROR] Directory not found: {directory_path}")
        return

    all_files = os.listdir(directory_path)
    image_files = [f for f in all_files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    # Process only new images
    for filename in image_files:
        full_path = os.path.join(directory_path, filename)
        if full_path in processed_set:
            print(f"[INFO] Skipping already processed: {full_path}")
            continue

        # Run OCR & LLM pipeline
        pipeline_ocr_and_llm(full_path, model=model)

        # Save processed status
        processed_set.add(full_path)
        try:
            with open(processed_log, "w", encoding="utf-8") as f:
                json.dump(list(processed_set), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to update processed log: {e}")

    print("[INFO] Done processing directory.")
