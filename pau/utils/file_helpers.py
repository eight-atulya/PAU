# pau/utils/file_helpers.py

import json
import os


def load_json(file_path, default_value=None):
    """
    Safely load a JSON file; if missing, create with default_value.
    """
    if not os.path.exists(file_path):
        if default_value is not None:
            save_json(file_path, default_value)
            return default_value
        else:
            return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(file_path, data):
    """ Safely save Python data as JSON. """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
