import sys

sys.path.insert(0, "../src")
from plate_model_manager import PlateModel, PlateModelManager

model_manager = PlateModelManager("../models.json")

# test remote models.json with URL
# model_manager = plate_model.PlateModelManager(
#    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
# )

model = model_manager.get_model("Muller2019")
model.set_data_dir("test-plate-model-folder")

print(model.get_avail_layers())

print(model.get_rotation_model())

print(model.get_layer("Coastlines"))

print(model.get_COBs())

print(model.get_topologies())

model.download_all_layers()

model.download_time_dependent_rasters("AgeGrids", times=[1, 2])

print(model.get_data_dir())

# this will download a large volume of data
# model.download_all()