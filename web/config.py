import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess string'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CHRONOS_ADMIN = os.environ.get('CHRONOS_ADMIN')

    CHRONOS_MAIL_SENDER = 'Chronos Team <chronos.dev.mail@gmail.com>'
    CHRONOS_MAIL_SUBJECT_PREFIX = '[Chronos]'

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/development'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/testing'

    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    pass

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql+psycopg2://postgres:secretpassword@localhost/postgres'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
