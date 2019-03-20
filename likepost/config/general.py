class BaseConfig:
    # SERVER_NAME = '0.0.0.0:8000'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
