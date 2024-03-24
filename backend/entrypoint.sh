python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py collectstatic
gunicorn core.wsgi:application --bind 0.0.0.0:8000
