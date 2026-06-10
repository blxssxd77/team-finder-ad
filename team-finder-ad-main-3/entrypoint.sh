#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py load_demo_data
gunicorn team_finder.wsgi:application --bind 0.0.0.0:8000
