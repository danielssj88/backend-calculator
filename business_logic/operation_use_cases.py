import requests
import configparser
import json
import re

from dao.DatabaseManager import DatabaseManager
from dao.OperationDao import OperationDao
from dao.RecordDao import RecordDao

cfg = configparser.ConfigParser()
cfg.read('config.ini')

db_manager = DatabaseManager.get_instance()
session = db_manager.get_session()


def statement_is_valid(statement):
    if statement == ':str':
        return True
    regex = r'^[\d.+\-*/\u221A]+$'
    if re.match(regex, statement):
        return True
    return False

def encode_square_root(statement):
    return statement.replace('\u221A', '')+'**0.5'

def get_random_string():
    response = requests.get(cfg['urls']['ramdom_string'])

    if response.status_code == 200:
        return response.text
    return 'ERROR GENERATING RANDOM STRING'

def get_operation(statement, operations):
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

def save_operation(user_id, statement, operations):
    if not statement_is_valid(statement):
        return (False, 'Invalid operation')
    if ':str' in statement:
        res = get_random_string()
        statement = 'random_string'
    else:
        encoded_statement = statement
        if '\u221A' in statement:
            encoded_statement = encode_square_root(statement)
        res = round(eval(encoded_statement), 2)
    operation = get_operation(statement, operations)
    record_dao = RecordDao(session)
    
    record = record_dao.get_recent_record_by_user(user_id)
    current_balance = record.user_balance if record else float(cfg['app']['initial_user_balance'])
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
    return (True, result)

def get_all_operations():
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
