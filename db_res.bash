sudo PGPASSWORD=postgres psql -U createdb dbdesarrollo --username=postgres --host=localhost --port=5432 -f ../itemmanagerdb_bk.sql
echo "Base de datos restaurada"
