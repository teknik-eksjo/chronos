Flask-example
=============

To bring up the project dependencies run.

.. code-block:: none

  docker-compose build
  docker-compose up -d

To bring up the development server run.

.. code-block:: none

  python3 -m venv venv
  . venv/bin/activate
  pip install -r requirements.txt
  ./manage.py runserver

To initialize the migration system run.

.. code-block:: none

  ./manage.py db init
  ./manage.py db commit -m "Initial commit message."

To initialize the database run.

.. code-block:: none

  ./manage.py deploy

To generate a new database migration run.

.. code-block:: none

  ./manage.py db commit -m "Commit message."
