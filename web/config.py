import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess string'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/postgres'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/postgres'


class ProductionConfig(Config):
    pass

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/postgres'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
