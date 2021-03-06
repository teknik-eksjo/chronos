from celery.utils.log import get_task_logger
from celery.exceptions import Retry
from . import create_celery_app
from . import db
from .models import User
from sqlalchemy.orm.exc import NoResultFound

celery = create_celery_app()
logger = get_task_logger(__name__)


@celery.task
def do_something(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()

        # Do something useful...
        logger.info('Fetched user {}'.format(user.id or '-'))

    except NoResultFound as e:
        logger.info('Failed to do something useful!')
        raise Retry(exc=e, when=10)
