from flask import Blueprint, request, jsonify
from pau.services.search_service import search_faiss

search_bp = Blueprint("search_bp", __name__)

@search_bp.route("/api/search/rag", methods=["POST"])
def search_rag():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = search_faiss(query, k=3)
    # Enrich each result with the document link here
    for r in results:
        r["document_link"] = f"/api/md-knowledge/{r['document']}"
    
    return jsonify({"results": results}), 200

