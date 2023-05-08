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

session = get_db_session()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

# Dummy database to store users
'''
users = {
    "admin": {
        "username": "admin",
        "password": generate_password_hash("password123"),
        "id": str(uuid.uuid4())
    }
}
'''

'''
operations = [
    {
        "id": 1,
        "type": "addition",
        "cost": 10.0
    },
    {
        "id": 2,
        "type": "addition",
        "cost": 10.0
    },
    {
        "id": 3,
        "type": "multiplication",
        "cost": 15.0
    },
    {
        "id": 4,
        "type": "division",
        "cost": 20.0
    },
    {
        "id": 5,
        "type": "square_root",
        "cost": 25.0
    },
    {
        "id": 6,
        "type": "random_string",
        "cost": 5.0
    }
]
'''

@api_v1.route('/operation', methods=['GET'])
@jwt_required()
def getOperations():
    operation_dao = OperationDao(session)
    operations = operation_dao.get_all()
    return jsonify(operations), 200

@api_v1.route('/record', methods=['GET'])
@jwt_required()
def getRecords():
    user_id = get_jwt_identity()
    record_dao = RecordDao(session)
    records = record_dao.get_records_by_user(user_id)
    return jsonify(records), 200

def statement_is_valid(statement):
    if statement == ':str':
        return True
    regex = r'^[\d.+\-*/\u221A]+$'
    if re.match(regex, statement):
        return True
    return False

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
    operation = [x for x in operations if x['type'] == operation_selected][0]
    return operation

def get_random_string():
    response = requests.get(cfg['urls']['ramdom_string'])

    if response.status_code == 200:
        return response.text
    return 'ERROR GENERATING RANDOM STRING'

@api_v1.route('/operation', methods=['POST'])
@jwt_required()
def saveOperation():
    user_id = get_jwt_identity()
    statement = request.json.get('statement')
    if not statement_is_valid(statement):
        return jsonify({'success': False, 'error': 'Invalid operation'}), 400
    if '\u221A' in statement:
        statement = statement.replace('\u221A', '')+'**0.5'
    if ':str' in statement:
        res = get_random_string()
        statement = 'random_string'
    else:
        res = eval(statement)
    operation = get_operation(statement)
    record_dao = RecordDao(session)
    
    record = record_dao.get_recent_record_by_user(user_id)
    new_balance = record['balance'] - operation['cost']
    
    record_dao.create_record(
        operation_id=operation['id'],
        user_id=user_id,
        amount=operation['cost'],
        user_balance=new_balance,
        operation_response=res,
        date=datetime.date.today()
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
    if not user or not check_password_hash(user.get('password'), password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    # Create an access token
    access_token = create_access_token(identity=user['id'])
    
    current_balance = 10000 # Get from DB
    
    response = {
        'access_token': access_token,
        'current_balance': current_balance
    }
    # Return the access token
    return jsonify(response), 200