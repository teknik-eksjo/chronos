from app import create_app
from app import db as _db
import pytest

def pytest_collection_modifyitems(items):
    """Handle custom markers.

    pytest hool called after test collection has been performed.

    Adds a marker named "gui" to enable filtering of tests.

    Args:
        items: list of _pytest.main.Node items, each item represents a test

    Reference:
        http://pytest.org/latest/plugins.html
    """
    for item in items:
        if 'live_server' in getattr(item, 'fixturenames', ()):
            item.add_marker('gui')


@pytest.fixture(scope='session')
def app():
    """Create an application context."""
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session wide database connection."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db

@pytest.fixture(scope='function')
def session(db, request):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
