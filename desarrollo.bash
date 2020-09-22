# Requisitos:
## git
## python3
#### pipenv
## postgres


echo "Clonando el repositorio"
git clone https://github.com/fer334/ItemManager/ || { echo "Error al clonar el repositorio" ; exit; }

echo "Ingresando al proyecto"
cd ItemManager || { echo "El directorio ItemManager no existe" ; exit; }

echo "Creando el entorno virtual e instalando las librerias necesarias"
pipenv install --dev || { echo "Error al crear el entorno virtual verfique la instalacion de pipenv"; exit;}

echo "Creando la base de datos itemmanagerdb (necesita permisos de administrador)"
sudo -u postgres PGPASSWORD=postgres createdb itemmanagerdb --username=postgres --host=localhost --port=5432 || {
  echo 'Posiblemente la base de datos itemmanagerdb ya exite, favor confirme esto con "si"'
  read -r -n 2 Respuesta;
  if [[ $Respuesta != "si" ]]
  then
    echo "Error al crear la base de datos";
    exit;
  fi
}

# TODO poblar la bd

echo "Limpiando cache de migraciones"
./clean_migrations.bash

echo "Realizando migraciones"
pipenv run ./manage.py makemigrations

echo "Migrando"
pipenv run ./manage.py migrate

echo "Corriendo el servidor"
pipenv run ./manage.py runserver
