from flask import Blueprint, send_from_directory, jsonify
import os

misc_bp = Blueprint("misc_bp", __name__)

@misc_bp.route("/api/md-knowledge/<path:filename>", methods=["GET"])
def serve_markdown(filename):
    # Compute the base directory relative to this file.
    # Since misc_routes.py is in pau/routes/, going up two levels should lead to the project root.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    docs_dir = os.path.join(base_dir, "database", "knowledge")
    
    file_path = os.path.join(docs_dir, filename)
    print("Attempting to serve file:", file_path)  # Debug print

    if os.path.exists(file_path):
        return send_from_directory(docs_dir, filename)
    else:
        return jsonify({"error": "File not found", "path": file_path}), 404
