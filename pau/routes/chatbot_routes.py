# pau/routes/chatbot_routes.py

from flask import Blueprint, request, jsonify
from networkx.readwrite import json_graph
from flask import send_from_directory
from pau.services.advanced_memory import store_advanced_memory, persist_advanced_memory



from pau.services.ai_engine import generate_chat_response
from pau.services.progress_service import increment_activity
from pau.services.chat_history_service import load_chat_history, save_chat_history
from pau.utils.system_prompt_loader import load_system_prompt
from pau.services.advanced_memory import (
    init_advanced_memory,
    store_advanced_memory,
    retrieve_advanced_memories,
    reward_memory,
    reduce_memory_importance,
    memory_graph,             # <-- import the actual graph
    find_related_nodes        # <-- for the entity-based route
)

chatbot_bp = Blueprint("chatbot_bp", __name__)


@chatbot_bp.route("/api/chat", methods=["POST"])
def api_chat():
    body = request.json
    if not body or "userMessage" not in body:
        return jsonify({"error": "Missing userMessage"}), 400

    user_message = body["userMessage"]
    prompt_type = body.get("promptType", "general")

    # Load system prompt
    system_prompt = load_system_prompt(prompt_type)

    # 1. Store user message in advanced memory
    store_advanced_memory(
        content=user_message,
        person="user",
        place="",
        time_label="now",
        importance=1.0
    )

    # 2. Retrieve relevant memories
    relevant_memories = retrieve_advanced_memories(query=user_message, top_k=3)

    memory_text = "\n".join([f"- {m['content']}" for m in relevant_memories])
    # Combine memory_text into final prompt
    # e.g., you might do: user_message + "\nMemories:\n" + memory_text

    # 3. Chat History
    chat_history = load_chat_history()
    messages = [{"role": "system", "content": system_prompt}] + chat_history
    messages.append({"role": "user", "content": user_message + "\nMemories:\n" + memory_text})

    try:
        data = generate_chat_response(messages)
        bot_reply = data["choices"][0]["message"]["content"]

        # Save chat history
        save_chat_history(user_message, bot_reply)

        # 4. Store AI reply
        store_advanced_memory(content=bot_reply, person="assistant")
        persist_advanced_memory()

        increment_activity("chat")

        return jsonify({"botReply": bot_reply}), 200

    except Exception as e:
        print("[ERROR] /api/chat =>", e)
        return jsonify({"error": "Failed to communicate with LLM"}), 500
    

@chatbot_bp.route("/api/chat/history", methods=["GET"])
def get_chat_history():
    """Returns the existing chat history."""
    return jsonify(load_chat_history()), 200


# ============ Memory Management Endpoints ============

@chatbot_bp.route("/api/memory/reward", methods=["POST"])
def api_memory_reward():
    """
    Expects JSON: { "docId": "<some doc id>", "rewardValue": 2.0 }
    Increases RL reward for that memory.
    """
    body = request.json
    doc_id = body.get("docId")
    reward_val = body.get("rewardValue", 1.0)
    reward_memory(doc_id, reward_val)
    return jsonify({"status": "ok", "docId": doc_id, "rewardAdded": reward_val})


@chatbot_bp.route("/api/memory/reduce", methods=["POST"])
def api_memory_reduce():
    """
    Expects JSON: { "docId": "<some doc id>", "penalty": 1.0 }
    Decreases RL reward for that memory.
    """
    body = request.json
    doc_id = body.get("docId")
    penalty = body.get("penalty", 0.1)
    reduce_memory_importance(doc_id, penalty)
    return jsonify({"status": "ok", "docId": doc_id, "penalty": penalty})


@chatbot_bp.route("/api/memory/graph/<string:entity>", methods=["GET"])
def api_memory_graph_entity(entity):
    """
    e.g. /api/memory/graph/bob => returns all connected nodes to 'bob'
    """
    neighbors = find_related_nodes(entity)
    return jsonify({"entity": entity, "neighbors": neighbors})

# ============ NEW ROUTE: Entire Graph ============

@chatbot_bp.route("/api/memory/graph", methods=["GET"])
def api_memory_graph():
    """
    Returns the entire memory graph in node-link JSON format for visualization.
    e.g. GET /api/memory/graph
    """
    data = json_graph.node_link_data(memory_graph)
    return jsonify(data), 200



@chatbot_bp.route("/graph_inspector", methods=["GET"])
def graph_inspector_page():
    return send_from_directory("public", "graph_inspector.html")

