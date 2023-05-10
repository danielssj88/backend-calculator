from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from business_logic.record_use_cases import get_records, filter_records
from . import api_record
from flask_restx import Api, Resource, fields

api_record_doc = Api(api_record)

user_model = api_record_doc.model('User', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(required=True, description='The username'),
    'status': fields.String(required=True, enum=['active', 'inactive'], description='The user status'),
})

operation_model = api_record_doc.model('Operation', {
    'id': fields.Integer(required=True, description='The operation identifier'),
    'type': fields.String(required=True, description='The operation type'),
    'cost': fields.Float(required=True, description='The operation cost'),
})

record_model = api_record_doc.model('Record', {
    'id': fields.Integer(required=True, description='The record identifier'),
    'operation_id': fields.Integer(required=True, description='The operation identifier'),
    'user_id': fields.Integer(required=True, description='The user identifier'),
    'amount': fields.Float(required=True, description='The amount of the operation'),
    'user_balance': fields.Float(required=True, description='The user balance after the operation'),
    'operation_response': fields.Nested(api_record_doc.model('OperationResponse', {
        'stmt': fields.String(required=True, description='The statement of the operation response'),
        'res': fields.String(required=True, description='The result of the operation response')
    }), required=False, description='The response of the operation'),
    'date': fields.DateTime(required=True, description='The date of the operation'),
    'operation': fields.Nested(api_record_doc.model('Operation', {
        'type': fields.String(required=True, description='The type of the operation')
    }), required=True, description='The operation information')
})


@api_record_doc.route('')
class Record(Resource):
    @jwt_required()
    @api_record_doc.doc(security='jwt')
    @api_record_doc.marshal_list_with(record_model)
    @api_record_doc.expect(api_record_doc.parser().add_argument('searchValue', type=str, help='The search value', required=False))
    def get(self, searchValue=None):
        user_id = get_jwt_identity()
        if searchValue:
            result = filter_records(user_id, searchValue)
        else:
            result = get_records(user_id)
        return result, 200
