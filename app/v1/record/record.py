from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business_logic.record_use_cases import get_records, filter_records
from . import api_record

@api_record.route('', methods=['GET'])
@jwt_required()
def getRecords():
    user_id = get_jwt_identity()
    result = get_records(user_id)
    return jsonify(result), 200

@api_record.route('/<searchValue>', methods=['GET'])
@jwt_required()
def filterRecords(searchValue):
    user_id = get_jwt_identity()
    result = filter_records(user_id, searchValue)
    return jsonify(result), 200
