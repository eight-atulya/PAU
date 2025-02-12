# pau/services/chat_history_service.py

import time
from pau.config import Config
from pau.utils.file_helpers import load_json, save_json

def load_chat_history():
    """Load chat history from JSON."""
    return load_json(Config.CHAT_HISTORY_FILE, default_value=[])

def save_chat_history(user_message, bot_reply):
    """Append messages to chat history and save."""
    chat_history = load_chat_history()
    now_timestamp = time.time()

    chat_history.append({"role": "user", "content": user_message, "timestamp": now_timestamp})
    chat_history.append({"role": "assistant", "content": bot_reply, "timestamp": time.time()})

    save_json(Config.CHAT_HISTORY_FILE, chat_history)
    return chat_history
