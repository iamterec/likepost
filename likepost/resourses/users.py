from flask_restful import Resource, reqparse
from models.user import User
from extensions import db

from sqlalchemy.exc import IntegrityError, DataError
from cerberus import Validator  # data validation

class Registration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

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
        except IntegrityError:
            return {"user": "User with this email already exist"}, 409
        except DataError:
            return {"error": "Too logn data"}, 403

        return {"msg": "User has been created",
                "user": user.to_dict()}, 200

    def validate_data(self, data):
        schema = {"email": {"required": True, "type": "string", "minlength": 6,
                            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"},
                  "password": {"required": True, "type": "string", "minlength": 3},
                  "username": {"required": False}}
        validator = Validator(schema)
        result = validator.validate(data)
        if not result:
            return validator.errors, 400
