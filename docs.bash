cd docs
rm -rvf source/_autosummary
make html
cd build/html
nohup xdg-open index.html > /dev/null
echo "Hace scroll hacia arriba y arregla todo los warnigs(las lineas de color rojooo)"