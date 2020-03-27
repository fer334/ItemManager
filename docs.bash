cd docs
rm -rvf source/_autosummary
make html
cd build/html
firefox index.html