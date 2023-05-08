from flask import Flask
from app.v1 import api_v1
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import configparser

# read config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    # Set up JWT
    app.config['JWT_SECRET_KEY'] = config['app']['jwt_secret_key']
    jwt = JWTManager(app)

    app.secret_key = config['app']['secret_key'] # TODO: Not sure if this line is required
    CORS(app)

    return app
