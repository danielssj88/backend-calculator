import json

from dao.DatabaseManager import DatabaseManager
from dao.RecordDao import RecordDao

db_manager = DatabaseManager.get_instance()
session = db_manager.get_session()

def format_records(result):
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

def get_records(user_id):
    record_dao = RecordDao(session)
    result = record_dao.get_records_by_user(user_id)
    return format_records(result)

def filter_records(user_id, searchValue):
    record_dao = RecordDao(session)
    result = record_dao.filter_records_by_user(user_id, searchValue)
    return format_records(result)