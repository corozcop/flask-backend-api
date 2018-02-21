from flask import Flask
from flask_restful import Resource, Api, reqparse
import logging.config
import settings
from resources.user import User, UserRegister

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = settings.JWT_SECRET_KEY

api = Api(app, prefix='/api/v1')

api.add_resource(User, '/users')
api.add_resource(UserRegister, '/register')

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=settings.FLASK_DEBUG)