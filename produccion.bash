#!/bin/bash

branch=$1
backupfile=$2
tag=$3
gitclone=$4

echo "Clonando el repositorio"

if [[ $gitclone == "true" ]]
then
    echo "Clonando el repositorio"
    git clone https://github.com/fer334/ItemManager/ || { echo "Error al clonar el repositorio" ; exit; }

    echo "Ingresando al proyecto"
    cd ItemManager || { echo "El directorio ItemManager no existe" ; exit; }
fi

git checkout $tag

echo "Loggeando en heroku"
heroku login
echo "Agregando el repositorio a la app"
heroku git:remote -a team-is2
echo "Reseteando la base de datos"
heroku pg:reset HEROKU_POSTGRESQL_RED_URL --confirm team-is2
echo "Realizando el push a la rama de heroku"
git push -f heroku HEAD:$branch
echo "Realizando migraciones"
heroku run "./manage.py makemigrations; ./manage.py migrate"
echo "Poblando la base de datos"
heroku pg:psql < $backupfile
heroku open
