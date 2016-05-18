import os
from celery.schedules import crontab


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess string'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql+psycopg2://postgres:secretpassword@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CHRONOS_ADMIN = os.environ.get('CHRONOS_ADMIN')

    CHRONOS_MAIL_SENDER = 'Chronos Team <chronos.dev.mail@gmail.com>'
    CHRONOS_MAIL_SUBJECT_PREFIX = '[Chronos]'

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Celery: Broker settings

    RABBITMQ_HOSTNAME = os.getenv('RABBITMQ_PORT_5672_TCP') or 'rabbitmq:5672'

    if RABBITMQ_HOSTNAME.startswith('tcp://'):
        RABBITMQ_HOSTNAME = RABBITMQ_HOSTNAME.split('//')[1]

    BROKER_URL = os.getenv('BROKER_URL') or 'amqp://{user}:{password}@{hostname}/{vhost}/'.format(
        user=os.getenv('RABBITMQ_DEFAULT_USER') or 'rabbitmq',
        password=os.getenv('RABBITMQ_DEFAULT_PASSWORD') or 'secretpassword',
        hostname=RABBITMQ_HOSTNAME,
        vhost=os.getenv('RABBITMQ_ENV_VHOST') or '')

    CELERYBEAT_SCHEDULE = {
        'remove-users-every-week': {
            'task': 'app.tasks.cleanup_inactive',
            'schedule': crontab(hour=2, minute=30, day_of_week=1),
            'args': ()
        },
    }

#    BROKER_HEARTBEAT = '?heartbeat=30'
#    if not BROKER_URL.endswith(BROKER_HEARTBEAT):
#        BROKER_URL += BROKER_HEARTBEAT

    BROKER_POOL_LIMIT = 1
    BROKER_CONNECTION_TIMEOUT = 10

    # Celery: Result backend settings

    CELERY_RESULT_BACKEND = os.getenv('RESULT_BACKEND') or 'redis://{hostname}:{port}/{db}'.format(
        hostname=os.getenv('REDIS_PORT_6379_TCP_ADDR') or 'redis',
        port=6379,
        db=0)

    # Celery: Basic settings

    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'UTC'

    CELERY_ALWAYS_EAGER = False
    CELERY_ACKS_LATE = True
    CELERY_TASK_PUBLISH_RETRY = True
    CELERY_DISABLE_RATE_LIMITS = False

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_RESULT_SERIALIZER = 'json'

    CELERYD_HIJACK_ROOT_LOGGER = False
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERYD_MAX_TASKS_PER_CHILD = 1000

    # List with all the modules containing tasks for celery

    CELERY_IMPORTS = ['app.tasks']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'postgresql+psycopg2://postgres:secretpassword@localhost/development'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'postgresql+psycopg2://postgres:secretpassword@localhost/testing'

    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    pass


class CeleryConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('CELERY_DATABASE_URI') or \
        'postgresql+psycopg2://postgres:secretpassword@postgresql/development'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'celery': CeleryConfig,

    'default': DevelopmentConfig
}
