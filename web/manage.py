#!/usr/bin/env python3
import os


if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


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


@manager.option('-h', '--no-html', dest='html', action='store_false',
                help='Do not generate html report.')
@manager.option('-r', '--no-report', dest='report', action='store_false',
                help='Do not generate report, only return with exit code.')
@manager.option('-g', '--gui', dest='gui', action='store_true',
                help='Run test with selenium.')
@manager.option('-c', '--coverage', dest='coverage', action='store_true',
                help='Run with coverage.py.')
def test(coverage, html, report, gui):
    """Run tests with py.test."""
    if coverage:
        # Initialize coverage.py.
        import coverage
        COV = coverage.coverage(branch=True, source=[APP_FOLDER])
        COV.start()

    # Run all unit tests found in tests folder.
    import pytest
    if gui:
        args = ['-v', 'tests']
    else:
        args = ['-v', 'tests', '-m', 'not gui']
    exit_code = pytest.main(args)

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


@manager.option('-s', '--stats', dest='stats', action='store_true',
                help='Lint and present statistics.')
@manager.option('-a', '--all', dest='all', action='store_true',
                help='Lint all files, even those outside of {}/.'.format(APP_FOLDER))
def lint(all, stats):
    """Run the linter."""
    from flake8 import main as flake8
    import sys

    if all:
        print('Running linter (including files outside of {}/).'.format(APP_FOLDER))
        sys.argv = ['flake8', '.']
    else:
        print('Running Linter...')
        sys.argv = ['flake8', APP_FOLDER]

    if stats:
        sys.argv.extend(['--statistics', '-qq'])

    flake8.main()


@manager.command
def sass():
    """Compile SASS files."""
    print('Compiling SASS files...')
    from sassutils import builder as sass

    sass.build_directory('app/static/sass', 'app/static/css')


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Role

    # Migrate database to latest revision
    upgrade()

    # Create user roles
    Role.insert_roles()


if __name__ == "__main__":
    manager.run()
