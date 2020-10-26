sudo PGPASSWORD=postgres psql -U postgres dbdesarrollo --host=localhost --port=5432 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
echo "Base de datos borrada"
