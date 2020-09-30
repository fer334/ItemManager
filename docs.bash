cd docs
rm -rvf source/_autosummary
make html
cd build/html
echo "Abriendo la documentacion con la app por defecto para html"
nohup xdg-open index.html > /dev/null
echo "Hace scroll hacia arriba y arregla todo los warnigs(las lineas de color rojooo)"
echo "Se creo el index en build/html/index.html"