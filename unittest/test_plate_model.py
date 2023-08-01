import sys

sys.path.insert(0, "../src")
from plate_model_manager import plate_model

model_manager = plate_model.PlateModelManager("../models.json")

# model_manager = plate_model.PlateModelManager(
#    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
# )

# model = plate_model.PlateModel("Muller2019", data_dir="test-plate-model-folder")

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

model.download_all(dst_path="./test-download-all")
