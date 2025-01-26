# pau/services/progress_service.py

from pau.config import Config
from pau.utils.file_helpers import load_json, save_json


def increment_activity(activity):
    """
    Increment usage count for a given activity (e.g. 'chat', 'search', 'notes').
    """
    data = load_json(Config.PROGRESS_FILE, default_value={
                     "chat": 0, "search": 0, "notes": 0})
    data[activity] = data.get(activity, 0) + 1
    save_json(Config.PROGRESS_FILE, data)


def get_progress():
    """Return dictionary with usage counts."""
    return load_json(Config.PROGRESS_FILE, default_value={"chat": 0, "search": 0, "notes": 0})
