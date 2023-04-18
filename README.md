# Finmancorp Python

Technical Review

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Basic Commands

### Setting Up Your Users

To create a **superuser account**, use this command:

    $ docker compose run --rm django python manage.py createsuperuser

### API Docs

You could check the Swagger Documentation

`{{host}}/api/docs/`

### Type checks

Running type checks with mypy:

    $ docker compose run --rm django mypy finmancorp_python

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ docker compose run --rm django coverage run -m pytest
    $ docker compose run --rm django coverage html
    $ docker compose run --rm django open htmlcov/index.html

#### Running tests with pytest

    $ docker compose run --rm django pytest -p no:warnings

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

## Pre-commit

### Instalación pre-commit

Virtualenv is required to be installed, if it is not installed, it can be installed as follows:

```bash
pip install virtualenv
```

Install a virtual environment and activate it:

```bash
virtualenv venv
```

Activation on Windows:

```bash
venv\Scripts\activate.bat
```

Activation on Unix/Linux:

```bash
. venv/bin/activate
```

Install pre-commit hooks to the local repository so they are triggered when committing and pushing:

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit run --all-files
```

To update pre-commit dependencies:

```bash
pre-commit autoupdate
pre-commit run --all-files
```

To execute on Linux:

```bash
pre-commit run all-files pip-compile || (($? == 0 || $1 == 1))
```
