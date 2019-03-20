from flask import Flask

from routes import connect_resources
from extensions import api, db

# Settings import
from config.general import DevelopmentConfig
from config.secret import SecretConfig


def create_app(settings_override=None):
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    app.config.from_object(SecretConfig)
    if settings_override:
        app.config.update(settings_override)

    connect_resources(api)
    init_extensions(app)
    # db.create_all()

    # CORS(app)
    return app


def init_extensions(app):
    api.init_app(app)
    api.app = app
    db.init_app(app)
    db.app = app

if __name__ == "__main__":
    create_app().run(debug=True, host='0.0.0.0', port='8000')
