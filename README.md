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

- `pmm ls -r https://www.earthbyte.org/webdav/ftp/gplately/models.json`
- `pmm download -m Muller2019 -p test-download`

#### Python script

```python
    from plate_model_manager import PlateModelManager
    pm_manager = PlateModelManager("https://www.earthbyte.org/webdav/ftp/gplately/models.json")
    model = pm_manager.get_model("Muller2019")
    model.download_all(dst_path="plate-models-data-dir")
```
