#### build doc

- `pip-compile pyproject.toml`
- `pip3 install .`
- `pip install -U sphinx sphinx_rtd_theme`
- `sphinx-apidoc -o doc/source src/plate_model_manager/`
- `make html`

⚠️You need to re-install the plate_model_manager, otherwise the sphinx will keep using the installed stable version(old code).
