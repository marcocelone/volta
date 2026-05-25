import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('is_admin',
        type=bool,
        default=False
    )

    def post(self):

        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': "User already exist!"}, 400

        user= UserModel(data['username'], data['password'], data.get('is_admin', False))
        try:
            user.save_to_db()
        except Exception:
            return {"message": "An error occurred creating the user"}, 500

        return {'message':'User created successfully'}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):

        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid credentials.'}, 401

        additional_claims = {'is_admin': user.is_admin}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        return {'access_token': access_token}, 200
