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

        if html:
            # Generate HTML report and move to tmp directory.
            import os
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)

        if report:
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


@manager.command
def seed():
    """Resets and creats new db, then fills the db with data to aid manual testing & debugging."""
    from datetime import datetime, timedelta, time
    from random import randint
    from flask_migrate import upgrade
    from app.models import (User,
                            Role,
                            WorkPeriod,
                            Schedule,
                            BaseSchedule,
                            Deviation,
                            Workday)

    NUMBER_OF_WORK_PERIODS = 2
    WORK_PERIOD_LENGTH = 90
    DEVIATIONS_PER_SCHEDULE = 3
    WORKDAYS_PER_BASE_SCHEDULE = 5

    db.drop_all()
    try:
        db.engine.execute('DROP TABLE alembic_version;')  # Dirty fix!
    except:
        pass
    upgrade()
    Role.insert_roles()

    def insert_work_periods(n, length):
        """Insert n subsequent work_periods.

        Params:
            n - Number of work_periods to insert
            length - Length of work_period (days)
        """
        for i in range(1, n + 1):
            start_date = datetime.now() - timedelta(days=i * length)
            end_date = datetime.now() - timedelta(days=(i - 1) * length)

            db.session.add(WorkPeriod(start=start_date, end=end_date))

    def insert_schedules(user_id):
        """Insert a schedule per work_period for a specic user.

        Each schedule contains:
            1 * base_schedule
            DEVIATIONS_PER_SCHEDULE * deviations

        Params:
            user_id - id of the target user
        """
        def generate_work_day(index, base_schedule_id):
            """Generate a work_day for a specific base_schedule."""
            db.session.add(Workday(index=index,
                                   base_schedule_id=base_schedule_id,
                                   start=time(hour=8),
                                   lunch_start=time(hour=11, minute=30),
                                   lunch_end=time(hour=12, minute=30),
                                   end=time(hour=16)))

        def generate_base_schedule(schedule_id):
            """Generate a base_schedule for a specific schedule."""
            db.session.add(BaseSchedule(schedule_id=schedule_id))

            base_schedule = BaseSchedule.query.filter_by(schedule_id=schedule_id).first()
            # Add work_days to the recently created base_schedule
            for index in range(WORKDAYS_PER_BASE_SCHEDULE):
                generate_work_day(index, base_schedule.id)

        def generate_deviation(schedule_id):
            """Generate a deviation for a specific schedule."""
            date = work_period.end - timedelta(days=randint(1, WORK_PERIOD_LENGTH))
            db.session.add(Deviation(schedule_id=schedule_id,
                                     date=date,
                                     start=time(hour=8),
                                     lunch_start=time(hour=11, minute=30),
                                     lunch_end=time(hour=12, minute=30),
                                     end=time(hour=16)))

        # Create a schedule for each work_period. Assuming that work_period_ids are integers
        for work_period_id in range(1, NUMBER_OF_WORK_PERIODS + 1):
            work_period = WorkPeriod.query.get(work_period_id)
            db.session.add(Schedule(user_id=user_id, work_period_id=work_period.id))

            schedule = Schedule.query.filter_by(work_period_id=work_period.id, user_id=user_id).first()
            # Add a base_schedule & some deviations to the recently created schedule
            generate_base_schedule(schedule.id)
            for deviation in range(DEVIATIONS_PER_SCHEDULE):
                generate_deviation(schedule.id)

    def insert_admin():
        """Insert an admin-account based on data from `.env`."""
        db.session.add(User(first_name=os.environ.get('CHRONOS_ADMIN_FIRST_NAME'),
                            last_name=os.environ.get('CHRONOS_ADMIN_LAST_NAME'),
                            email=os.environ.get('CHRONOS_ADMIN'),
                            password=os.environ.get('CHRONOS_ADMIN_PASSWORD')))

    def insert_teachers():
        """Insert some teachers."""
        first_names = ['Carl', 'Daniel', 'Gustav', 'Britt', 'Marie', 'Ulla-Carin']
        last_names = ['Svensson', 'Itzler', 'Wilde', 'Birgersson', 'Stjärnberg', 'Johansson' ]
        emails = ['carl@banan.se', 'daniel.itzler@hotmail.nu', 'gustavwilde@live.se', 'britt_brigersson68@google.se', 'Marie1789@mex.nu', 'ullacarin45@hej.se']

        def generate_last_seen_date():
            """Generate a 'last_seen'-date."""
            td = timedelta(days=randint(30, 90), hours=randint(1, 24), minutes=randint(1, 59))
            return datetime.now() - td

        for i in range(len(first_names)):
            db.session.add(User(first_name=first_names[i],
                                last_name=last_names[i],
                                email=emails[i],
                                last_seen=generate_last_seen_date()))

            # Add a schedule to the recently created teacher
            user = User.query.filter_by(email=emails[i]).first()
            insert_schedules(user.id)

    insert_admin()
    insert_work_periods(NUMBER_OF_WORK_PERIODS, WORK_PERIOD_LENGTH)
    insert_teachers()
    db.session.commit()


if __name__ == "__main__":
    manager.run()
