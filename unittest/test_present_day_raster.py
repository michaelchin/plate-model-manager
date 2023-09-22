#!/usr/bin/env python
import os
import sys
import unittest


sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR, get_test_logger

from plate_model_manager import PresentDayRasterManager

if __name__ == "__main__":
    logger_name = "test_present_day_raster_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)


class RasterTestCase(unittest.TestCase):
    def setUp(self):
        self.manager = PresentDayRasterManager("../present_day_rasters.json")
        # self.manager = PresentDayRasterManager("")
        self.manager.set_data_dir(TEMP_TEST_DIR)

    def test_present_day_raster(self):
        rasters = self.manager.list_present_day_rasters()
        self.assertTrue(len(rasters) > 0)
        logger.info(rasters)
        raster_file = self.manager.get_raster("TOPOGRAPHY")
        self.assertTrue(os.path.isfile(raster_file))


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(RasterTestCase("test_present_day_raster"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(RasterTestCase))
