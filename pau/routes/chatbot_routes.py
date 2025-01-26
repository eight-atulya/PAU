# pau/routes/chatbot_routes.py

import time
from flask import Blueprint, request, jsonify
from pau.services.ai_engine import generate_chat_response
from pau.services.progress_service import increment_activity
from pau.config import Config
from pau.utils.file_helpers import load_json, save_json

chatbot_bp = Blueprint("chatbot_bp", __name__)


@chatbot_bp.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Expects JSON: { "userMessage": "Hello" }
    Returns: { "botReply": "..." }
    """
    body = request.json
    if not body or "userMessage" not in body:
        return jsonify({"error": "Missing userMessage"}), 400

    user_message = body["userMessage"]

    # Load existing chat history (optional for multi-turn context)
    chat_history = load_json(Config.CHAT_HISTORY_FILE, default_value=[])

    messages = [
        {"role": "system", "content": "You are Intelligent MI"},
        {"role": "user", "content": user_message}
    ]

    try:
        data = generate_chat_response(messages)
        bot_reply = data["choices"][0]["message"]["content"]

        # Persist chat in chatHistory.json
        now_timestamp = time.time()
        chat_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": now_timestamp
        })
        chat_history.append({
            "role": "assistant",
            "content": bot_reply,
            "timestamp": time.time()
        })
        save_json(Config.CHAT_HISTORY_FILE, chat_history)

        # Update progress for chat usage
        increment_activity("chat")

        return jsonify({"botReply": bot_reply}), 200

    except Exception as e:
        print("[ERROR] /api/chat =>", e)
        return jsonify({"error": "Failed to communicate with LM Studio"}), 500
