import os
import json
from flask import Blueprint, request, jsonify

landing_bp = Blueprint('landing_bp', __name__)

@landing_bp.route('/api/get_user', methods=['GET'])
def get_user():
    """
    Return the stored user name from user_data.json.
    """
    user_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'user_data.json')
    if os.path.exists(user_data_path):
        with open(user_data_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"name": ""})

@landing_bp.route('/api/set_user', methods=['POST'])
def set_user():
    """
    Store/update the user name in user_data.json.
    """
    user_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'user_data.json')
    
    # Extract name from request body
    payload = request.get_json(force=True)
    name = payload.get('name', '').strip()

    # Save to JSON
    with open(user_data_path, 'w') as f:
        json.dump({"name": name}, f)

    return jsonify({"success": True, "name": name})
