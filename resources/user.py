from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
import re
from models.user import UserModel
import datetime


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('full_name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
        email = data['email']
        if UserModel.find_by_email(email):
            return {"message": "Email already registered"}, 409
        match = re.match(regex, str(email.lower()))
        if not match:
            return {"message": "Invalid Email"}, 400

        newuser = UserModel(data['full_name'], data['email'], data['password'])
        msg = newuser.save_to_db()

        if msg:
            return msg, 500
        return {'message': 'User created successfully', 'user': newuser.json()}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="username cannot be blank")
    parser.add_argument('password', type=str, required=True, help="password cannot be blank")

    def post(self):
        data = UserLogin.parser.parse_args()
        username = data['username']
        password = data['password']
        user  = UserModel.find_by_email(username)
        if not user:
            user = UserModel.find_by_username(username)
            if not user:
                return {"message": "Invalid credentials"}, 404
        if not user.check_password(password):
            return {"message": "Invalid credentials"}, 404
        api_token = create_access_token(identity=user.uuid, expires_delta=datetime.timedelta(hours=12))
        return {'user': user.json(), 'token': api_token}


class User(Resource):
    def get(self):
        return {'users': [u.json() for u in UserModel.query.all()]}