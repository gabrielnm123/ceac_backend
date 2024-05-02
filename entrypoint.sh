#!/bin/bash

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput
cp staticfiles /staticfiles
gunicorn core.wsgi:application --bind 0.0.0.0:8000
