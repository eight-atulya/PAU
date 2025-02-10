# pau/routes/misc_routes.py (example new route)
from flask import Blueprint, jsonify, send_from_directory
import os

landing_bp = Blueprint("landing_bp", __name__)

@landing_bp.route("/api/boxes", methods=["GET"])
def get_boxes_data():
    """
    Returns the contents of boxes_data.json
    """
    file_path = os.path.join("database", "boxes_data.json")
    if not os.path.exists(file_path):
        return jsonify({"error": "boxes_data.json not found"}), 404

    import json
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return jsonify(data), 200


@landing_bp.route("/api/md/<filename>", methods=["GET"])
def serve_markdown(filename):
    """
    Serves a markdown file from the database/docs directory
    """
    docs_dir = os.path.join("database", "docs")
    return send_from_directory(docs_dir, filename)

