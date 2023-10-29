# plate-model-manager

![build workflow](https://github.com/michaelchin/plate-model-manager/actions/workflows/build.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/plate-model-manager.svg)](https://badge.fury.io/py/plate-model-manager)
![anaconda_badge](https://anaconda.org/conda-forge/plate-model-manager/badges/version.svg)
![platforms](https://anaconda.org/conda-forge/plate-model-manager/badges/platforms.svg)
![downloads](https://anaconda.org/conda-forge/plate-model-manager/badges/downloads.svg)

This is a dataset manager for plate tectonic models. It is similar to NPM or Conda for software packages.

### How to install

`pip install plate-model-manager`

### How to use

#### command line

- `pmm ls`
  This will list all available reconstruction models, such as
  - muller2019
  - muller2022
  - muller2016
  - merdith2021
  - matthews2016
  - matthews2016_mantle_ref
  - matthews2016_pmag_ref
  - domeier2014
  - golonka
  - pehrsson2015
  - paleomap
  - torsvikcocks2017
  - rodinia
  - seton2012
- `pmm download -m Muller2019 -p test-download`
  This will download model "Muller2019" into a folder 'test-download'.

#### Python script

```python
    from plate_model_manager import PlateModelManager

    pm_manager = PlateModelManager()
    model = pm_manager.get_model("Muller2019")
    model.set_data_dir("plate-models-data-dir")
    print(model.get_rotation_model())
```

    ['plate-models-data-dir/muller2019//Rotations/Muller2019-Young2019-Cao2020.rot']

The above Python code download the "Muller2019" model. The model.get_rotation_model() function gets the rotation file location.

### Examples

This Python module is Mostly used in [GPlately](https://github.com/GPlates/gplately) and [GPlates Web Service](https://github.com/GPlates/gplates-web-service). The usage example can be found at https://github.com/GPlates/gplately/blob/master/tests-dir/pytestcases-pmm/conftest.py.
