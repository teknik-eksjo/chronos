from app import create_app
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


@pytest.fixture
def app():
    """Create an application context."""
    app = create_app('testing')
    return app
