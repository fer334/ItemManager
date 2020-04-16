sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo pg_dump -U fer itemmanagerdb --username=postgres --host=localhost --port=5432 -a > ../itemmanagerdb_bk.sql
