import configparser
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from dao import get_db_session
from dao.UserDao import UserDao
from dao.RecordDao import RecordDao

cfg = configparser.ConfigParser()
cfg.read('config.ini')

session = get_db_session()


def user_login(username, password):
    user_dao = UserDao(session)
    user = user_dao.get_user_by_username(username)
    if not user or not check_password_hash(user.password, password):
        return (False, 'Invalid credentials')

    record_dao = RecordDao(session)
    record = record_dao.get_recent_record_by_user(user.id)
    current_balance = record.user_balance if record else cfg['app']['initial_user_balance']
    access_token = create_access_token(identity=user.id)

    response = {
        'access_token': access_token,
        'current_balance': current_balance
    }
    return (True, response)