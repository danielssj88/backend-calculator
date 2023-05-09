from flask import request, jsonify
from business_logic.user_use_cases import user_login
from . import api_login

@api_login.route('', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    success, response = user_login(username, password)
    if not success:
        return jsonify({'success': False, 'error': response}), 401
    return jsonify(response), 200
