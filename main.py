from app import create_app
from flask_restx import Api, Resource

app = create_app()
api = Api(app)

@api.route('/swagger')
class Swagger(Resource):
    def get(self):
        return api.__schema__

if __name__ == '__main__':
    app.run(debug=True)
