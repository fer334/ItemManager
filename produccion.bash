#!/bin/bash


branch=$1
backupfile=$2

git push heroku $branch

heroku run echo "Limpiando cache de migraciones"
heroku run ./clean_migrations.bash

heroku run echo "Realizando migraciones"
heroku run ./manage.py makemigrations
heroku run python manage.py migrate

heroku pg:psql < $backupfile
gunicorn ItemManager.wsgi

