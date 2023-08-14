import sys

sys.path.insert(0, "../src")
from plate_model_manager import PlateModel


model = PlateModel("Muller2019", readonly=True)

print(model.get_avail_layers())

print(model.get_rotation_model())

print(model.get_layer("Coastlines"))

print(model.get_COBs())

print(model.get_topologies())

print(model.get_data_dir())
