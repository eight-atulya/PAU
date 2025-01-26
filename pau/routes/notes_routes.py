# pau/routes/notes_routes.py

from flask import Blueprint, request, jsonify
from pau.services.notes_service import list_notes, get_note_content, save_note_content
from pau.services.progress_service import increment_activity

notes_bp = Blueprint("notes_bp", __name__)


@notes_bp.route("/api/notes", methods=["GET"])
def list_all_notes():
    try:
        notes = list_notes()
        return jsonify({"notes": notes}), 200
    except Exception as e:
        print("[ERROR] /api/notes =>", e)
        return jsonify({"error": "Unable to list notes"}), 500


@notes_bp.route("/api/notes/<note_name>", methods=["GET"])
def get_note(note_name):
    content = get_note_content(note_name)
    if content is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"content": content}), 200


@notes_bp.route("/api/notes", methods=["POST"])
def save_note():
    body = request.json
    if not body or "noteName" not in body or "noteContent" not in body:
        return jsonify({"error": "noteName and noteContent are required"}), 400

    note_name = body["noteName"]
    note_content = body["noteContent"]
    try:
        save_note_content(note_name, note_content)
        increment_activity("notes")
        return jsonify({"message": f"Note '{note_name}' saved successfully."}), 200
    except Exception as e:
        print("[ERROR] /api/notes =>", e)
        return jsonify({"error": "Unable to save note"}), 500
