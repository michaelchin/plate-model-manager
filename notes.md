#### activate/deactivate the python virtual env

- `python -m venv plate-model-manager-venv`
- `source plate-model-manager-venv/bin/activate`
- `pip install -r requirements.txt `
- `deactivate`

#### build and install the package

- `pip3 install pip-tools`
- `pip-compile pyproject.toml`
- `pip3 install .`

#### test

- The file .env must be in current working directory. Alternatively you can set the env variables instead.

#### doc

- `pip-compile pyproject.toml`
- `pip3 install .`
- `pip install -U sphinx sphinx_rtd_theme`
- `sphinx-apidoc -o doc/source src/plate_model_manager/`
- `make html`

⚠️You need to re-install the plate_model_manager, otherwise the sphinx will keep using the installed stable version(old code).

#### Publish to PyPI

- `pip install build twine`
- `python -m build`
- `twine check dist/*`
- `twine upload -r testpypi dist/*`
- `twine upload dist/*`
