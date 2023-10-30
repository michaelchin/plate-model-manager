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

#### Use the command line

- `pmm ls`
  This command will list all available reconstruction models, such as
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
- `pmm ls Muller2019`
  This command will show the details of model 'Muller2019'.
- `pmm download Muller2019 plate-models-data-dir`
  This command will download model "Muller2019" into a folder 'plate-models-data-dir'.
- `pmm download all`
  This command will download all available models into the current working directory.

#### Use in Python script

```python
    # print all available model names
    from plate_model_manager import PlateModelManager

    m_manager = PlateModelManager()
    for name in pm_manager.get_available_model_names():
      print(name)
```

```python
    from plate_model_manager import PlateModelManager

    pm_manager = PlateModelManager()
    model = pm_manager.get_model("Muller2019")
    model.set_data_dir("plate-models-data-dir")
    model.download_all_layers()
    print(model.get_rotation_model())
```

    ['plate-models-data-dir/muller2019//Rotations/Muller2019-Young2019-Cao2020.rot']

The above Python code download the "Muller2019" model. The model.get_rotation_model() function returns the rotation file location.

### Examples

This Python module is mostly used in [GPlately](https://github.com/GPlates/gplately), [GPlates Web Service](https://github.com/GPlates/gplates-web-service) and [PyGPlates Tutorials](https://github.com/GPlates/pygplates-tutorials).

A good example of using PlateModelManager with PyGPlates can be found [here](https://github.com/GPlates/pygplates-tutorials/blob/master/notebooks/working-with-plate-model-manager.ipynb).
