from flask import request
from flask_restx import Api, Resource, Namespace, fields

from business_logic.user_use_cases import user_login
from . import api_login
api_login_doc = Api(api_login)


login_fields = api_login_doc.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

class Login(Resource):
    @api_login_doc.expect(login_fields, validate=True)
    @api_login_doc.doc(responses={401: 'Invalid credentials'})
    def post(self):
        """User login"""
        username = request.json.get('username')
        password = request.json.get('password')
        success, response = user_login(username, password)
        if not success:
            return {'success': False, 'error': response}, 401
        return response, 200

api_login_doc.add_resource(Login, '/login')
