# stack-overflow-api
This application allows to filter and get the stack overflow questions.

### Dependencies
* Python 3.8
* Django 3.0
* pipenv
* pytest

### Setup Instructions 
* Rename .env.sample to .env
* pipenv install --python 3.8
* pipenv shell
* python manage.py migrate
* python manage.py runserver

### Run Tests
* pipenv install --dev
* pytest
