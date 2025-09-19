#!/bin/bash
cd backend
python manage.py collectstatic --noinput
gunicorn myproject.wsgi --bind 0.0.0.0:$PORT --log-file -