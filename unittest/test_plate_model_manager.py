import sys

sys.path.insert(0, "../src")
from plate_model_manager import PlateModelManager

model_manager = PlateModelManager("../models.json")
print(model_manager.get_available_model_names())
print(model_manager.get_model("Muller2019"))
print(model_manager.get_model("no-good-model"))

print("*******************************************************")

# test remote models.json with URL
model_manager = PlateModelManager(
    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
)
print(model_manager.get_available_model_names())
print(model_manager.get_model("Muller2019"))
print(model_manager.get_model("no-good-model"))
