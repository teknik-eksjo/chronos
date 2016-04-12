Chronos Development
===================

Most commands should be run in the `web` directory.

To bring up the project dependencies run (in the project root directory).

.. code-block:: none

  docker-compose build
  docker-compose up -d

To initialize the development venv.

.. code-block:: none

  python3 -m venv venv
  . venv/bin/activate
  pip install -r requirements.txt

To bring up the development server run.

.. code-block:: none

  ./manage.py runserver

Database migrations
-------------------

Database migrations are handled by `Flask-migrate <https://flask-migrate.readthedocs.org/en/latest/>`_.

To initialize the database run.

.. code-block:: none

  ./manage.py deploy

To generate a new database migration run.

.. code-block:: none

  ./manage.py db migrate -m "Commit message."

Before creating the first database migration you must initialize the system.

.. code-block:: none

  ./manage.py db init


Tests
-----

Tests uses Selenium and requires the default driver (Firefox).

.. code-block:: None

  ./manage.py test
