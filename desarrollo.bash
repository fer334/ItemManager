#!/bin/bash

# Requisitos:
## git
## python3
#### pipenv
## postgres

dbname="$1"
username="$2"
pass="$3"
filename="$4"
port="$5"
gitclone="$6"

if [[ $gitclone == "true" ]]
then
    echo "Clonando el repositorio"
    git clone https://github.com/fer334/ItemManager/ || { echo "Error al clonar el repositorio" ; exit; }

    echo "Ingresando al proyecto"
    cd ItemManager || { echo "El directorio ItemManager no existe" ; exit; }
fi

echo "Creando el entorno virtual e instalando las librerias necesarias"
pipenv install --dev || { echo "Error al crear el entorno virtual verfique la instalacion de pipenv"; exit;}

echo "Creando la base de datos $dbname (necesita permisos de administrador)"

sudo -u postgres PGPASSWORD=$pass createdb $dbname --username=$username --host=localhost --port=$port || {
  echo 'Posiblemente la base de datos '$dbname' ya exite, favor confirme esto con "si"'
  read -r -n 2 Respuesta;
  if [[ $Respuesta != "si" ]]
  then
    echo "Error al crear la base de datos";
    exit;
  fi
}

echo "Modificando las configuraciones de django"
sed -i -e "0,/'NAME'/s/:.*/: '$dbname'/" ItemManager/settings.py
sed -i -e "0,/'USER'/s/:.*/: '$username'/" ItemManager/settings.py
sed -i -e "0,/'PASSWORD'/s/:.*/: '$pass'/" ItemManager/settings.py


echo "Limpiando cache de migraciones"
./clean_migrations.bash

echo "Realizando migraciones"
pipenv run ./manage.py makemigrations

echo "Migrando"
pipenv run ./manage.py migrate

echo "Poblando la base de datos"
sudo PGPASSWORD=$pass psql -U createdb $dbname --username=$username --host=localhost --port=$port -f $filename ||{
    pwd
    echo "Error al poblar la base de Datos";
    exit;
}

echo "Corriendo el servidor"
pipenv run ./manage.py runserver

