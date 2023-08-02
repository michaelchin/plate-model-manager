#!/bin/bash

#assume the working directory is the root of this repository

pip3 install build twine
python -m build
twine check dist/*

pip3 install pip-tools
pip3 install -U sphinx sphinx_rtd_theme
pip-compile pyproject.toml
pip3 install .
rm doc/source/plate_model_manager.rst
rm doc/source/modules.rst
sphinx-apidoc -o doc/source src/plate_model_manager/
cd doc
make html