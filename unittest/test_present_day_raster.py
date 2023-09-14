import sys

sys.path.insert(0, "../src")
from plate_model_manager import PresentDayRasterManager

manager = PresentDayRasterManager("../present_day_rasters.json")
# manager = PresentDayRasterManager("")
print(manager.list_present_day_rasters())
manager.get_raster("test_xz")
manager.get_raster("test_gz")
manager.get_raster("test_lzma")
manager.get_raster("test_bz2")
manager.get_raster("test_tar_gz")
manager.get_raster("test_tgz")
manager.get_raster("test_txz")
manager.get_raster("test_tbz2")
manager.get_raster("test_tar_xz")
manager.get_raster("test_tar_bz2")
