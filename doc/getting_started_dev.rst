Getting Started with Shoop Development
======================================

.. note::

   If you are planning on using Shoop for developing your own shop,
   read the :doc:`other Getting Started guide <getting_started>` instead.

Installation for Shoop Development
----------------------------------

To start developing Shoop, you'll need a Git checkout of Shoop and a
Github fork of Shoop for creating pull requests.  Github pull requests
are used to get your changes into Shoop Base.

 1. If you haven't done so already, create a fork of Shoop in Github by
    clicking the "Fork" button at https://github.com/shoopio/shoop and
    clone the fork to your computer as usual. See `Github Help about
    forking repos <https://help.github.com/articles/fork-a-repo/>`__ for
    details.

 2. Setup a virtualenv and activate it.  You may use the traditional
    ``virtualenv`` command, or the newer ``python -m venv`` if you're
    using Python 3.  See `Virtualenv User Guide
    <https://virtualenv.pypa.io/en/latest/userguide.html>`__, if you
    don't know virtualenv already.  For example, following commands
    create and activate a virtualenv in Linux:

    .. code-block:: shell

       virtualenv shoop-venv
       . shoop-venv/bin/activate

 3. Finally, you'll need to install Shoop in the activated virtualenv in
    development mode.  To do that, run the following commands in the
    root of the checkout (within the activated virtualenv):

    .. code-block:: shell

       pip install -e .
       python setup.py build_resources

Workbench, the built-in test project
------------------------------------

The Workbench project in the repository is a self-contained Django
project set up to use an SQLite database. It is used by the test suite
and is also useful for development on its own.

Practically the only difference to a normal Django project is that instead
of ``python manage.py``, one uses ``python -m shoop_workbench``.

To get started with Workbench, invoke the following in the Shoop working copy
root.

.. code-block:: shell

   # Migrate database.
   python -m shoop_workbench migrate

   # Import some basic data.
   python -m shoop_workbench shoop_populate_mock --with-superuser=admin

   # Run the Django development server (on port 8000 by default).
   python -m shoop_workbench runserver

You can use the credentials ``admin``/``admin``, that is username ``admin``
and password ``admin`` to log in as a superuser on http://127.0.0.1:8000/ .

Building resources
------------------

Shoop uses JavaScript and CSS resources that are compiled using various
Node.js packages.  These resources are compiled automatically by
``setup.py`` when installing Shoop with pip, but if you make changes to
the source files (e.g. under ``shoop/admin/static_src``), the resources
have to be rebuilt.

This can be done with

.. code-block:: shell

   python setup.py build_resources

The command also accepts couple arguments, see its help for more details:

.. code-block:: shell

   python setup.py build_resources --help

Running tests
-------------

To run tests in the active virtualenv:

.. code-block:: shell

   py.test -v shoop_tests
   # Or with coverage
   py.test -vvv --cov shoop --cov-report html shoop_tests

To run tests for all supported Python versions run:

.. code-block:: shell

   pip install tox  # To install tox, needed just once
   tox

Docstring coverage
------------------

The DocCov script is included for calculating some documentation coverage metrics.

.. code-block:: shell

   python _misc/doccov.py shoop/core -o doccov.html

Translations
------------

All translations are under ``shoop/core/locale``.

To add new translations for existing strings, just edit the relevant ``shoop/core/locale/<code>/LC_MESSAGES/django.po``
file.

If you add new translatable strings to the code, you will need to first extract the translation strings to be able
to edit them in other languages. For this, use the ``pybabel`` command as follows, executed from git root.

To extract strings, first generate a template:

.. code-block:: shell

   pybabel extract -F babel.cfg -o locales.pot shoop/

Then update message files by executing this:

.. code-block:: shell

   pybabel update -D django -d shoop/core/locale -i locales.pot

Then you can edit the changed ``.po`` files with new translations, or just commit the new message files so someone
else can translate them.

To make changes to translation files available to your local installation, compile the messages:

.. code-block:: shell

   pybabel compile -D django -d shoop/core/locale
