#!/usr/bin/env python3
import os

from app import create_app, db, models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

APP_FOLDER = 'app'


# Implement manage.py shell
def make_shell_context():  # noqa
    return dict(app=app, db=db, models=models)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False, html=True, report=True):
    """Run the tests."""
    if coverage:
        # Initialize coverage.py.
        import coverage
        COV = coverage.coverage(branch=True, source=[APP_FOLDER])
        COV.start()

    # Run all unit tests found in tests folder.
    import pytest
    exit_code = pytest.main(['-v', 'tests'])

    if coverage:
        # Sum up the results of the code coverage analysis.
        COV.stop()
        COV.save()

        if not html:
            # Generate HTML report and move to tmp directory.
            import os
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)

        if not report:
            # Show the report and clean up.
            print('\nCoverage Summary\n{}'.format('=' * 70))
            COV.report()
            COV.erase()

    raise SystemExit(exit_code)


@manager.command
def lint(all=False, stats=False):
    """Run the linter."""
    from flake8 import main as flake8
    import sys

    if all:
        print('Running linter (including skeleton code).')
        sys.argv = ['flake8', '.']
    else:
        print('Running Linter...')
        sys.argv = ['flake8', APP_FOLDER]

    if stats:
        sys.argv.extend(['--statistics', '-qq'])

    flake8.main()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # Migrate database to latest revision
    upgrade()


if __name__ == "__main__":
    manager.run()
