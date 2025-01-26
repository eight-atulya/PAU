# pau/routes/progress_routes.py

from flask import Blueprint, jsonify
from pau.services.progress_service import get_progress

progress_bp = Blueprint("progress_bp", __name__)


@progress_bp.route("/api/progress", methods=["GET"])
def get_user_progress():
    try:
        data = get_progress()
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/progress =>", e)
        return jsonify({"error": "Unable to read progress"}), 500
