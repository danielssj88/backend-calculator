from flask import request, jsonify
from flask_caching import Cache
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Api, Namespace, Resource, fields

from business_logic.operation_use_cases import save_operation, get_all_operations
from . import api_operation

api_operation_doc = Api(api_operation)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

def init_cache(app):
    cache.init_app(app)

operation_model = api_operation_doc.model('Operation', {
    'id': fields.Integer(required=True, description='The operation ID'),
    'type': fields.String(required=True, description='The type of operation'),
    'cost': fields.Float(required=True, description='The cost of the operation')
})

@api_operation_doc.route('', methods=['GET', 'POST'])
class Operation(Resource):
    @jwt_required()
    @api_operation_doc.doc(description='Get all operations')
    @api_operation_doc.marshal_list_with(operation_model)
    def get(self):
        """Get all operations"""
        operations = get_cached_operations()
        return operations, 200

    @jwt_required()
    @api_operation_doc.doc(description='Save an operation')
    @api_operation_doc.response(400, 'Bad request')
    def post(self):
        """Save an operation"""
        user_id = get_jwt_identity()
        statement = request.json.get('statement')
        operations = get_cached_operations()
        success, response = save_operation(user_id, statement, operations)
        if not success:
            return {'success': False, 'error': response}, 400
        return response, 200

@cache.cached(timeout=50, key_prefix='get_cached_operations')
def get_cached_operations():
    return get_all_operations()

api_operation_doc.add_resource(Operation, '/operation')
