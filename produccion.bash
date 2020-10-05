#!/bin/bash


branch=$1
backupfile=$2
tag=$3

echo "Clonando el repositorio"
git clone https://github.com/fer334/ItemManager/ || { echo "Error al clonar el repositorio" ; exit; }

echo "Ingresando al proyecto"
cd ItemManager || { echo "El directorio ItemManager no existe" ; exit; }

git checkout $tag

echo "Loggeando en heroku"
heroku login
echo "Realizando el push a la rama de heroku"
git push heroku $branch:$tag
echo "Poblando la base de datos"
heroku pg:psql < $backupfile

