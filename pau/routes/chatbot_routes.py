# pau/routes/chatbot_routes.py

from flask import Blueprint, request, jsonify
from pau.services.ai_engine import generate_chat_response
from pau.services.progress_service import increment_activity
from pau.services.chat_history_service import load_chat_history, save_chat_history
from pau.utils.system_prompt_loader import load_system_prompt  # Import our new function

chatbot_bp = Blueprint("chatbot_bp", __name__)

@chatbot_bp.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Expects JSON: { "userMessage": "Hello", "promptType": "developer_assistant" }
    Returns: { "botReply": "..." }
    """
    body = request.json
    if not body or "userMessage" not in body:
        return jsonify({"error": "Missing userMessage"}), 400

    user_message = body["userMessage"]
    prompt_type = body.get("promptType", "general")  # Default to "general" if not provided

    # Load the system prompt dynamically
    system_prompt = load_system_prompt(prompt_type)

    # Load chat history
    chat_history = load_chat_history()

    # Construct the message list
    messages = [{"role": "system", "content": system_prompt}] + chat_history
    messages.append({"role": "user", "content": user_message})

    try:
        # Generate AI response
        data = generate_chat_response(messages)
        bot_reply = data["choices"][0]["message"]["content"]

        # Save chat history
        save_chat_history(user_message, bot_reply)

        # Update progress tracking
        increment_activity("chat")

        return jsonify({"botReply": bot_reply}), 200

    except Exception as e:
        print("[ERROR] /api/chat =>", e)
        return jsonify({"error": "Failed to communicate with LLM"}), 500


@chatbot_bp.route("/api/chat/history", methods=["GET"])
def get_chat_history():
    """Returns the existing chat history."""
    return jsonify(load_chat_history()), 200