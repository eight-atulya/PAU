from pau.services.ocr_llm_pipeline import pipeline_ocr_and_llm

image_path = "data/screen_snapshot/DigitalVision_monitor1_20250211_185544.png"

pipeline_ocr_and_llm(image_path, model="llama-3.2-1b-instruct")
