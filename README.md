# plate-model-manager

![build workflow](https://github.com/michaelchin/plate-model-manager/actions/workflows/build.yml/badge.svg)

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