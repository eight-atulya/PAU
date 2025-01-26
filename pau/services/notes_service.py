# pau/services/notes_service.py

import os
from pau.config import Config
from pau.utils.file_helpers import load_json, save_json


def list_notes():
    """Return all .md files in the notes directory."""
    files = os.listdir(Config.NOTES_DIR)
    return [f for f in files if f.endswith(".md")]


def get_note_content(note_name):
    """Read a note file content."""
    file_path = os.path.join(Config.NOTES_DIR, note_name)
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_note_content(note_name, content):
    """Save note content to a file."""
    file_path = os.path.join(Config.NOTES_DIR, note_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
