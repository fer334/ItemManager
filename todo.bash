./db_bk.bash
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Borrar archivos cache!!!"
read
./clean_migrations.bash
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Borrar la db!!!"
read
./db_rm.bash
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Realizar migraciones !!"
read
./manage.py makemigrations
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Migrar!!"
read
./manage.py migrate
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Restore db!!"
read
./db_res.bash
echo "=> Enter para continuar, CTRL+C para cancelar. Siguiente accion: Correr el servidor!!"
read
./manage.py runserver

#sudo dropdb itemmanagerdb --username=postgres --host=localhost --port=5432 -e