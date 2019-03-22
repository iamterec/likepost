import datetime
from flask_restful import Resource, reqparse
from models.user import User
from extensions import db

from sqlalchemy.exc import IntegrityError, DataError
from cerberus import Validator  # data validation
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

from tasks.users import get_aditional_data_for_user

CLEARBIT = True
EMAILHUNTER = False

class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str)
    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)

    def post(self):
        data = self.parser.parse_args()
        user = User(data["email"], data["username"])
        user.set_password(data["password"])

        validation = self.validate_data(data)
        if validation:
            return validation, 422

        try:
            db.session.add(user)
            db.session.commit()
            if CLEARBIT:
                get_aditional_data_for_user.delay(user=user.to_dict(username=True))
        except IntegrityError:
            db.session.rollback()
            return {"user": "User with this email already exist"}, 409
        except DataError:
            db.session.rollback()
            return {"error": "The data is too long"}, 403

        return {"msg": "User has been created",
                "user": user.to_dict()}, 200

    def validate_data(self, data):
        schema = {"email": {"required": True, "type": "string", "minlength": 6,
                            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"},
                  "password": {"required": True, "type": "string", "minlength": 3},
                  "username": {"required": False, 'nullable': True}}
        validator = Validator(schema)
        result = validator.validate(data)
        if not result:
            return validator.errors, 400

    def delete(self):
        '''Only for convience purposes. It is not the part of the REST API'''
        data = self.parser.parse_args()
        user = User.query.filter(User.email == data["email"]).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"user": "User has been deleted"}, 200


class UserMe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str)
    parser.add_argument("password", type=str)

    @jwt_required
    def get(self):
        user_identity = get_jwt_identity()
        user = User.query.filter(User.email == user_identity["email"]).first()
        if user:
            return {"user": user.to_dict()}
        else:
            return {"error": "User not found"}, 404

    @jwt_required
    def delete(self):
        data = self.parser.parse_args()
        user = User.query.filter(User.email == data["email"]).first()
        if user and user.check_password(data["password"]):
            db.session.delete(user)
            db.session.commit()
            return {"user": "User has been deleted"}, 200
        else:
            return {"msg": "Wrong credentials"}, 422


class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

    def post(self):
        data = self.parser.parse_args()
        user = User.query.filter(User.email == data["email"]).first()
        if user and user.check_password(data["password"]):
            identity = user.to_dict(username=False)
            expires = datetime.timedelta(seconds=178800)
            access_token = create_access_token(identity=identity, expires_delta=expires)
            return {"access_token": access_token}, 200
        else:
            return {"msg": "Wrong e-mail or password"}, 422
