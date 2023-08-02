#### build doc

- `pip-compile pyproject.toml`
- `pip3 install .`
- `sphinx-apidoc -o doc/source src/geoserver_pyadm/`
- `make html`

⚠️You need to re-install the geoserver_pyadm, otherwise the sphinx will keep using the installed stable version(old code).