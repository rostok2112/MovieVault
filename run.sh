#!/bin/sh


set -ex # fail on any error and enable print of debug logs

python manage.py  migrate # Migrate DB
python manage.py collectstatic # Collect static
python manage.py runserver 8005 --deploy # Run application
