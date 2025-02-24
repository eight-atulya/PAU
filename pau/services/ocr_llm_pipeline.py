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

def generate_response(user_prompt, system_prompt=None, model="llama-3.2-1b-instruct"):
    """
    If system_prompt is provided, we add it as the system role message.
    Then we add the user prompt as the user role message.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # user message
    messages.append({"role": "user", "content": user_prompt})

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
# 2) OCR FUNCTION
##################################
def run_ocr(image_path: str) -> str:
    """
    Uses Tesseract to extract text from an image.
    Returns the recognized text (or empty string on error).
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed for {image_path}: {e}")
        return ""

##################################
# 3) STORE PROCESSED RESULT
##################################
def store_ocr_llm_result(image_path: str, final_text: str, output_folder="data/processed_logs"):
    """
    Creates a .md file referencing the image and storing the final text from the LLM.
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
def pipeline_ocr_and_llm(image_path: str, model="llama-3.2-1b-instruct"):
    """
    1) Run OCR on the image.
    2) Use local LLM to parse the raw text into meaningful text.
    3) Store the final text with link to the image in data/processed_logs.
    """
    print(f"[INFO] Starting OCR + LLM pipeline for {image_path}")

    # Step 1: OCR
    raw_text = run_ocr(image_path)
    if not raw_text:
        print("[WARN] OCR returned empty text. Possibly no text or an error.")
        # continue or return, up to you

    # Step 2: LLM parse
    prompt = f"Please parse and summarize the following text:\n\n{raw_text}"
    final_text = generate_response(prompt, model=model)
    if not final_text:
        print("[WARN] LLM parse returned empty. Possibly an error or no meaningful parse.")

    # Step 3: Store
    store_ocr_llm_result(image_path, final_text, output_folder="data/processed_logs")

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
    1) Loads the set of already processed images from processed_log.
    2) Iterates over all .png/.jpg in directory_path.
    3) If an image is not in the processed set, runs pipeline_ocr_and_llm.
    4) Adds that image to the processed set and saves the log.
    """
    # Step A: Load processed set
    processed_set = set()
    if os.path.exists(processed_log):
        try:
            with open(processed_log, "r", encoding="utf-8") as f:
                processed_list = json.load(f)
            processed_set = set(processed_list)
        except Exception as e:
            print(f"[ERROR] Could not read {processed_log}: {e}")
            # fallback to empty set

    # Step B: Gather images from directory
    if not os.path.exists(directory_path):
        print(f"[ERROR] Directory not found: {directory_path}")
        return

    all_files = os.listdir(directory_path)
    image_files = [f for f in all_files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    # Step C: Process each image if not in processed_set
    for filename in image_files:
        full_path = os.path.join(directory_path, filename)
        if full_path in processed_set:
            print(f"[INFO] Skipping already processed: {full_path}")
            continue

        # Not processed, run pipeline
        pipeline_ocr_and_llm(full_path, model=model)

        # Add to processed_set
        processed_set.add(full_path)

        # Save updated log
        try:
            with open(processed_log, "w", encoding="utf-8") as f:
                json.dump(list(processed_set), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to update processed log: {e}")

    print("[INFO] Done processing directory.")
