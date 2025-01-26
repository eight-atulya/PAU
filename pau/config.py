# pau/config.py

import os


class Config:
    # Example: You can read from env or just hard-code for local dev
    LMSTUDIO_API_URL = os.getenv(
        "LMSTUDIO_API_URL", "http://127.0.0.1:1234/v1/chat/completions")
    SEARXNG_API_URL = os.getenv(
        "SEARXNG_API_URL", "http://localhost:8080/search")

    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    NOTES_DIR = os.path.join(DATA_DIR, "notes")
    CHAT_HISTORY_FILE = os.path.join(DATA_DIR, "chatHistory.json")
    PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

    # etc.
