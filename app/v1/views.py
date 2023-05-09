from flask import request, jsonify
from flask_caching import Cache
from flask_jwt_extended import jwt_required, get_jwt_identity
import configparser

from . import api_v1
from dao import get_db_session
from business_logic.user_use_cases import user_login
from business_logic.operation_use_cases import save_operation, get_all_operations
from business_logic.record_use_cases import get_records, filter_records

session = get_db_session()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def init_cache(app):
    cache.init_app(app)

@api_v1.route('/operation', methods=['GET'])
@jwt_required()
def getOperations():
    operations = get_cached_operations()
    return jsonify(operations), 200

@api_v1.route('/record', methods=['GET'])
@jwt_required()
def getRecords():
    user_id = get_jwt_identity()
    result = get_records(user_id)
    return jsonify(result), 200

@api_v1.route('/record/<searchValue>', methods=['GET'])
@jwt_required()
def filterRecords(searchValue):
    user_id = get_jwt_identity()
    result = filter_records(user_id, searchValue)
    return jsonify(result), 200

@cache.cached(timeout=50, key_prefix='get_cached_operations')
def get_cached_operations():
    return get_all_operations()

@api_v1.route('/operation', methods=['POST'])
@jwt_required()
def saveOperation():
    user_id = get_jwt_identity()
    statement = request.json.get('statement')
    operations = get_cached_operations()
    success, response = save_operation(user_id, statement, operations)
    if not success:
        return jsonify({'success': False, 'error': response}), 400
    return jsonify(response), 200

# Login endpoint
@api_v1.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    success, response = user_login(username, password)
    if not success:
        return jsonify({'success': False, 'error': response}), 401
    return jsonify(response), 200