from config import config
from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


bootstrap = Bootstrap()
csrf = CsrfProtect()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
moment = Moment()


def create_app(config_name):
    """Application factory, see docs_.

    .. _docs: http://flask.pocoo.org/docs/0.10/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if app.config.get('DEBUG'):
        from sassutils.wsgi import SassMiddleware

        app.wsgi_app = SassMiddleware(app.wsgi_app, {'app': ('static/sass', 'static/css', '/static/css')})

    bootstrap.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app


def create_celery_app(app=None):
    import os
    app = app or create_app('celery')
    celery = Celery(__name__)
    celery.config_from_object(config['celery'])

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
