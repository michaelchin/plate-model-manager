import sys

sys.path.insert(0, "../src")
from plate_model_manager import PresentDayRasterManager

manager = PresentDayRasterManager("../present_day_rasters.json")
# manager = PresentDayRasterManager("")
print(manager.list_present_day_rasters())
manager.get_raster("TOPOGRAPHY_xz")
