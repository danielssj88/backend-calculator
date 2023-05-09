from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business_logic.operation_use_cases import save_operation, get_all_operations
from . import api_operation

@api_operation.route('', methods=['GET'])
@jwt_required()
def getOperations():
    operations = get_cached_operations()
    return jsonify(operations), 200

@api_operation.route('', methods=['POST'])
@jwt_required()
def saveOperation():
    user_id = get_jwt_identity()
    statement = request.json.get('statement')
    operations = get_cached_operations()
    success, response = save_operation(user_id, statement, operations)
    if not success:
        return jsonify({'success': False, 'error': response}), 400
    return jsonify(response), 200

def get_cached_operations():
    return get_all_operations()