#!/bin/bash


branch=$1
backupfile=$2

echo "Realizando el push a la rama de heroku"
git push heroku $branch
echo "Poblando la base de datos"
heroku pg:psql < $backupfile

