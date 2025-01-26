# pau/routes/search_routes.py

from flask import Blueprint, request, jsonify
from pau.services.search_service import perform_search
from pau.services.progress_service import increment_activity

search_bp = Blueprint("search_bp", __name__)


@search_bp.route("/api/search", methods=["GET"])
def api_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    try:
        data = perform_search(query)
        # data["results"] => list of search results from SearXNG
        results = []
        for r in data.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", "")
            })

        # Increment usage
        increment_activity("search")

        return jsonify({"results": results}), 200
    except Exception as e:
        print("[ERROR] /api/search =>", e)
        return jsonify({"error": "Failed to fetch search results"}), 500
