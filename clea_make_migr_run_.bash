echo "Eliminando migraciones y caches"
echo "..."
rm -rfv `find . -name 0*.py`
rm -rfv `find . -name __p*`
echo "Vaciado"

./manage.py makemigrations
./manage.py migrate
./manage.py runserver