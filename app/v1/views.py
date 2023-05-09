from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import re
import datetime
import requests

from dao.UserDao import UserDao
from dao.RecordDao import RecordDao
from dao.OperationDao import OperationDao

from . import api_v1
import configparser
from dao import get_db_session
from flask_caching import Cache
import json

session = get_db_session()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

INITIAL_DEFAULT_BALANCE = 10000

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def init_cache(app):
    cache.init_app(app)

@api_v1.route('/operation', methods=['GET'])
@jwt_required()
def getOperations():
    operations = get_cached_operations()
    return jsonify(operations), 200

def get_records(result):
    records = []
    for row in result:
        records.append({
            'id': row.id,
            'operation': row.operation.type,
            'amount': row.amount,
            'user_balance': row.user_balance,
            'operation_response': json.loads(row.operation_response),
            'date': row.date
        })
    return records

@api_v1.route('/record', methods=['GET'])
@jwt_required()
def getRecords():
    user_id = get_jwt_identity()
    record_dao = RecordDao(session)
    result = record_dao.get_records_by_user(user_id)
    return jsonify(get_records(result)), 200

@api_v1.route('/record/<searchValue>', methods=['GET'])
@jwt_required()
def filterRecords(searchValue):
    user_id = get_jwt_identity()
    record_dao = RecordDao(session)
    result = record_dao.filter_records_by_user(user_id, searchValue)
    return jsonify(get_records(result)), 200

def statement_is_valid(statement):
    if statement == ':str':
        return True
    regex = r'^[\d.+\-*/\u221A]+$'
    if re.match(regex, statement):
        return True
    return False

@cache.cached(timeout=50, key_prefix='get_cached_operations')
def get_cached_operations():
    operation_dao = OperationDao(session)
    response = operation_dao.get_all()
    operations = []
    for row in response:
        operations.append({
            'id': row.id,
            'type': row.type,
            'cost': row.cost
        })
    return operations

def get_operation(statement):
    operation_selected = ''
    if '+' in statement:
        operation_selected = 'addition'
    elif '-' in statement:
        operation_selected = 'substraction'
    elif '*' in statement:
        operation_selected = 'multiplication'
    elif '/' in statement:
        operation_selected = 'division'
    elif '\u221A' in statement:
        operation_selected = 'square_root'
    elif 'random_string' in statement:
        operation_selected = 'random_string'
    operations = get_cached_operations()
    operation = [x for x in operations if x['type'] == operation_selected][0]
    return operation

def get_random_string():
    response = requests.get(cfg['urls']['ramdom_string'])

    if response.status_code == 200:
        return response.text
    return 'ERROR GENERATING RANDOM STRING'

def encode_square_root(statement):
    return statement.replace('\u221A', '')+'**0.5'

@api_v1.route('/operation', methods=['POST'])
@jwt_required()
def saveOperation():
    user_id = get_jwt_identity()
    statement = request.json.get('statement')
    if not statement_is_valid(statement):
        return jsonify({'success': False, 'error': 'Invalid operation'}), 400
    if ':str' in statement:
        res = get_random_string()
        statement = 'random_string'
    else:
        encoded_statement = statement
        if '\u221A' in statement:
            encoded_statement = encode_square_root(statement)
        res = round(eval(encoded_statement), 2)
    operation = get_operation(statement)
    record_dao = RecordDao(session)
    
    record = record_dao.get_recent_record_by_user(user_id)
    current_balance = record.user_balance if record else INITIAL_DEFAULT_BALANCE
    new_balance = current_balance - operation['cost']
    operation_response = json.dumps({
        'stmt': statement,
        'res': res
    })
    
    record_dao.create_record(
        operation_id=operation['id'],
        user_id=user_id,
        amount=operation['cost'],
        user_balance=new_balance,
        operation_response=operation_response
    )
    
    result = {
        'result': res,
        'balance': new_balance
    }
    
    return jsonify(result), 200

# Login endpoint
@api_v1.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user_dao = UserDao(session)
    user = user_dao.get_user_by_username(username)
    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    # Create an access token
    access_token = create_access_token(identity=user.id)

    record_dao = RecordDao(session)
    record = record_dao.get_recent_record_by_user(user.id)
    current_balance = record.user_balance if record else INITIAL_DEFAULT_BALANCE

    response = {
        'access_token': access_token,
        'current_balance': current_balance
    }
    # Return the access token
    return jsonify(response), 200