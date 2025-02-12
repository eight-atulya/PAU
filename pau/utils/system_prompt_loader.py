# pau/utils/system_prompt_loader.py

import os

SYSTEM_PROMPT_DIR = "database/system_prompts"

def load_system_prompt(prompt_name="general"):
    """
    Loads a system prompt from a markdown file.
    :param prompt_name: Name of the markdown file (without extension).
    :return: The content of the system prompt file.
    """
    prompt_path = os.path.join(SYSTEM_PROMPT_DIR, f"{prompt_name}.md")

    if not os.path.exists(prompt_path):
        print(f"[WARNING] System prompt '{prompt_name}.md' not found. Using default prompt.")
        return "You are a helpful AI assistant."

    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()
