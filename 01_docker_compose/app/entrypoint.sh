#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

python manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser --noinput 
fi
python manage.py collectstatic
gunicorn movies.wsgi:application --bind 0.0.0.0:8000

# exec "$@"