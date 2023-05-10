from flask import Blueprint
from flask_restx import Api

from .login import api_login
from .operation import api_operation
from .record import api_record

from .login.login import api_login_doc, Login
from .operation.operation import api_operation_doc, Operation
from .record.record import api_record_doc, Record


api_v1 = Blueprint('api_v1', __name__)
api_v1.register_blueprint(api_login)
api_v1.register_blueprint(api_operation)
api_v1.register_blueprint(api_record)

api_v1_doc = Api(api_v1, doc='/docs')
api_v1_doc.add_namespace(api_login_doc)
api_v1_doc.add_namespace(api_operation_doc)
api_v1_doc.add_namespace(api_record_doc)

api_v1_doc.add_resource(Login, '/login')
api_v1_doc.add_resource(Operation, '/operation')
api_v1_doc.add_resource(Record, '/record')


'''
from .login import login
from .operation import operation
from .record import record
'''
