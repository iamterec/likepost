from flask_restful import Resource, reqparse


class Registration(Resource):

    def get(self):
        return "Hello from registration resource"
