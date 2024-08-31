# plate-model-manager

![unittest](https://github.com/michaelchin/plate-model-manager/actions/workflows/unittest.yml/badge.svg)
![unittest-win](https://github.com/michaelchin/plate-model-manager/actions/workflows/unittest-win.yml/badge.svg)
![build-doc](https://github.com/michaelchin/plate-model-manager/actions/workflows/build-doc-update-gh-pages.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/plate-model-manager.svg)](https://badge.fury.io/py/plate-model-manager)
![anaconda_badge](https://anaconda.org/conda-forge/plate-model-manager/badges/version.svg)
![platforms](https://anaconda.org/conda-forge/plate-model-manager/badges/platforms.svg)
![downloads](https://anaconda.org/conda-forge/plate-model-manager/badges/downloads.svg)

Originally the plate-model-manager was designed for [GPlately](https://github.com/GPlates/gplately). Later, it was found also useful in other scenarios and contexts. The plate-model-manager downloads and manages the plate reconstruction model files. It is a dataset manager for plate tectonic reconstruction models, similar to NPM or Conda for software packages.

Have you ever wondered where to get the plate tectonic reconstruction models for your research? Are you tired of downloading files from Internet manually and specify file paths when calling PyGPlates functions? If the answer is yes, you probably want to check out this plate-model-manager Python module.

### How to install

`pip install plate-model-manager`

### How to use

#### Basic Usage

👉 The Python code below downloads the "Muller2019" model into local folder "plate-models-data-dir" and returns the rotation file's location.

```python
from plate_model_manager import PlateModelManager

print(PlateModelManager().get_model("Muller2019",data_dir="plate-models-data-dir").get_rotation_model())
```

![python print rotation screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-python-print-rotation.png)

👉 The Python code below lists all available reconstruction models.

```python
from plate_model_manager import PlateModelManager

print(PlateModelManager().get_available_model_names())
```

![python list all models screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-python-list-all-models.png)

#### Use PMM with pyGPlates 🌰

```python
pm_manager = PlateModelManager()
model = pm_manager.get_model("Muller2019")

# create a point feature at (0,0)
point_feature = pygplates.Feature()
point_feature.set_geometry(pygplates.PointOnSphere(0, 0))

# assign plate ID
point_feature_with_PID = pygplates.partition_into_plates(
  model.get_static_polygons(), # 👈👀 LOOK HERE
  model.get_rotation_model(), # 👈👀 LOOK HERE
  [point_feature])

# Reconstruct the point features.
reconstructed_feature_geometries = []
time=140
pygplates.reconstruct(
  point_feature_with_PID,
  model.get_rotation_model(), # 👈👀 LOOK HERE
  reconstructed_feature_geometries,
  time)

print(reconstructed_feature_geometries[0].get_reconstructed_geometry().to_lat_lon())
```

See the full example at https://github.com/GPlates/pygplates-tutorials/blob/master/notebooks/working-with-plate-model-manager.ipynb

#### Use PMM with GPlately 🌰

```python
pm_manager = PlateModelManager()
model = pm_manager.get_model("Muller2019")
model.set_data_dir("plate-model-repo")

age = 55
test_model = PlateReconstruction(
    model.get_rotation_model(), # 👈👀 LOOK HERE
    topology_features=model.get_layer("Topologies"), # 👈👀 LOOK HERE
    static_polygons=model.get_layer("StaticPolygons"), # 👈👀 LOOK HERE
)
gplot = PlotTopologies(
    test_model,
    coastlines=model.get_layer("Coastlines"), # 👈👀 LOOK HERE
    COBs=model.get_layer("COBs"), # 👈👀 LOOK HERE
    time=age,
)
```

See the full example at https://github.com/GPlates/gplately/blob/master/Notebooks/Examples/working-with-plate-model-manager.py

#### Use the command line

- `pmm ls`

  This command will list all available plate tectonic reconstruction models.

  ![pmm ls command screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-pmm-ls-command.png)

- `pmm ls Muller2019`

  This command will show the details of model 'Muller2019'.

  ![pmm ls model command screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-pmm-ls-model.png)

- `pmm download Muller2019 plate-models-data-dir`

  This command will download model "Muller2019" into a folder 'plate-models-data-dir'.

  ![pmm download model screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-pmm-download-model.png)

- `pmm download all`

  This command will download all available models into the current working directory.

  ![pmm download all screenshot](https://github.com/michaelchin/plate-model-manager/raw/main/images/screenshot-pmm-download-all.png)

### Examples

This Python module is mostly used in 

- [GPlately](https://github.com/GPlates/gplately)
- [GPlates Web Service](https://github.com/GPlates/gplates-web-service)
- [PyGPlates Tutorials](https://github.com/GPlates/pygplates-tutorials)
- [GWS Python Wrapper](https://github.com/michaelchin/gwspy)

A good example of using PlateModelManager with PyGPlates can be found at 

- https://github.com/GPlates/pygplates-tutorials/blob/master/notebooks/working-with-plate-model-manager.ipynb.

The examples of using PlateModelManager with GPlately:

- https://github.com/GPlates/gplately/blob/master/Notebooks/Examples/introducing-plate-model-manager.py
- https://github.com/GPlates/gplately/blob/master/Notebooks/Examples/working-with-plate-model-manager.py

The PlateModelManager can also be used with the GPlates desktop. Use the command line to download the plate model files and open the files with GPlates desktop. This will save the trouble of downloading files from Internet manually.

### Dependencies

- aiohttp
- requests
- nest_asyncio

### Event loop RuntimeError

For Jupyter Notebook, Web Server or GUI application users, you need the following two lines to workaround the event loop RuntimeError.
If you do not add these two lines, the PlateModelManager still works. But you will see a warning message. You can ignore the warning message safely.
If the warning message bothers you, add the two lines before calling PlateModelManager.

https://anaconda.org/conda-forge/nest-asyncio/

```python
import nest_asyncio
nest_asyncio.apply()
```
