from flask import Flask

# Settings import
from config.general import DevelopmentConfig
from config.secret import SecretConfig

from flask_restful import Api

from resourses.users import Registration

def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    app.config.from_object(SecretConfig)

    # connect_resources(api)
    api = Api()
    api.add_resource(Registration, "/users")
    # db.create_all()

    api.init_app(app)
    api.app = app

    # CORS(app)
    return app


if __name__ == "__main__":
    create_app().run(debug=True, host='0.0.0.0', port='8000')
