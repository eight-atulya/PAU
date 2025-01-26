import os
import json


def load_json(file_path, default_value):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_value, f)
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def update_progress(activity):
    progress = load_json('data/progress.json',
                         {"chat": 0, "search": 0, "notes": 0})
    progress[activity] = progress.get(activity, 0) + 1
    save_json('data/progress.json', progress)
