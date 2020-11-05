sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo PGPASSWORD=postgres pg_dump -U postgres dbdesarrollo --host=localhost --port=5432 -a > ../itemmanagerdb_bk.sql
echo "Backup sobre la base de datos finalizada"
