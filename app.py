from flask import Flask
from flask_restful import Resource, Api, reqparse
import logging.config
import settings
from resources.user import User, UserRegister, UserLogin
from resources.group import GroupsList, Groups
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
app.secret_key = settings.JWT_SECRET_KEY
jwt = JWTManager(app)

api = Api(app, prefix='/api/v1')

api.add_resource(User, '/users')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(GroupsList, '/groups')
api.add_resource(Groups, '/group', '/group/<string:_id>')

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    log.info('>>>>>> Starting development server at http://{}/api/v1<<<<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)