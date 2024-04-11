python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:8000
