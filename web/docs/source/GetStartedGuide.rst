Getting Started
===============

Setup Chronos for development
-----------------------------

The first step when setting up Chronos is to clone the repository:

.. code-block:: bash
    
    git clone https://github.com/teknik-eksjo/chronos.git

Create a virtual python environment, activate it and install the python project requirements:

.. code-block:: bash
    
    cd chronos/web
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

If needed, also install docker-compose:

.. code-block:: bash

    pip install docker-compose

From the root directory of the project, bring up the project dependencies:

.. code-block:: bash

    docker-compose build
    docker-compose up -d

Create a .env-file in the web directory. This file is used to set environment variables and the following are needed to use and run chronos:

.. code-block:: bash
    
    DEV_DATABASE_URI=postgresql+psycop2://postgres:secretpassword@localhost/development
    TEST_DATABASE_URI=postgresql+psycopg2://postgres:secretpassword@localhost/testing
    CHRONOS_ADMIN=email@email.com
    CHRONOS_ADMIN_FIRST_NAME=Firstname
    CHRONOS_ADMIN_LAST_NAME=Lastname
    CHRONOS_ADMIN_PASSWORD=password
    BROKER_URL=amqp://rabbitmq:secretpassword@localhost//
    RESULT_BACKEND=redis://localhost:6379/0

.. note:: If you are using a Mac with Docker Toolbox for development, :code:`localhost` should be replaced with the current docker ip.

          |  :code:`CHRONOS_ADMIN` sets the administrator account email adress.
          |  :code:`CHRONOS_ADMIN_FIRST_NAME` sets the administrator account firstname.
          |  :code:`CHRONOS_ADMIN_LAST_NAME` sets the administrator account lastname.
          |  :code:`CHRONOS_ADMIN_PASSWORD` sets the administrator account password.

Initialize the database in the web directory:

.. code-block:: bash
    
    cd web
    ./manage.py deploy

To generate "dummy"-data run:

.. code-block:: bash

    ./manage.py seed

To bring up the development server run:

.. code-block:: bash

    ./manage.py runserver


Database migrations
-------------------

Database-migrations are handled by Flask-migrate_.

.. _Flask-migrate: https://flask-migrate.readthedocs.org/en/latest/

The database are initalized by running:

.. code-block:: bash

    ./manage.py deploy

To generate a new database migration run:

.. code-block:: bash

    ./manage.py db migrate -m "Commit message."

Before creating the **first** database migration run:

.. code-block:: bash

    ./manage.py db init

Tests
-----

Tests can be run with the following command:

.. code-block:: bash

    ./manage.py test

If there's tests that use Selenium they can be run with --gui:

.. code-block:: bash
    
    ./manage.py test --gui

Linting can be run with the following command:

.. code-block:: bash

    ./manage.py lint

Environment Variables
---------------------

The file .env in the web directory can be used to set environment variables. The environment variables can be seen in the config.py file. The file **should** consist of the following in order for chronos to function:

.. code-block:: bash
    
    DEV_DATABASE_URI=postgresql+psycop2://postgres:secretpassword@localhost/development
    TEST_DATABASE_URI=postgresql+psycopg2://postgres:secretpassword@localhost/testing
    CHRONOS_ADMIN=email@email.com
    CHRONOS_ADMIN_FIRST_NAME=Firstname
    CHRONOS_ADMIN_LAST_NAME=Lastname
    CHRONOS_ADMIN_PASSWORD=password
    BROKER_URL=amqp://rabbitmq:secretpassword@localhost//
    RESULT_BACKEND=redis://localhost:6379/0

:code:`MAIL_USERNAME`  and :code:`MAIL_PASSWORD` needs to be set in order to use the email functionality
(the credentials are according to the config.py-file supposed to be for sendgrid.com. This can be changed.).