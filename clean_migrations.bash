echo "Eliminando migraciones y caches"
echo "..."
rm -rfv `find . -name 0*.py`
rm -rfv `find . -name __p*`
echo "..."
echo "Listo para realizar las migraciones" 