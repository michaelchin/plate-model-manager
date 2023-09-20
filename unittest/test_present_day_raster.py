#!/usr/bin/env python
import os
import sys

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR

from plate_model_manager import PresentDayRasterManager


def main():
    manager = PresentDayRasterManager("../present_day_rasters.json")
    # manager = PresentDayRasterManager("")
    manager.set_data_dir(TEMP_TEST_DIR)
    print(manager.list_present_day_rasters())
    print(manager.get_raster("TOPOGRAPHY"))


if __name__ == "__main__":
    main()
