from flask import Blueprint
from .login import api_login
from .operation import api_operation
from .record import api_record

api_v1 = Blueprint('api_v1', __name__)
api_v1.register_blueprint(api_login, url_prefix='/login')
api_v1.register_blueprint(api_operation, url_prefix='/operation')
api_v1.register_blueprint(api_record, url_prefix='/record')

from .login import login
from .operation import operation
from .record import record
