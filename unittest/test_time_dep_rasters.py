#!/usr/bin/env python3

import os
import sys
import unittest


sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR, get_test_logger

from plate_model_manager import PlateModelManager

if __name__ == "__main__":
    logger_name = "test_time_dep_rasters_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)


class TimeDepRastersTestCase(unittest.TestCase):
    def setUp(self):
        model_manager = PlateModelManager(f"{os.path.dirname(__file__)}/../models.json")

        # test remote models.json with URL
        # model_manager = plate_model.PlateModelManager(
        #    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
        # )
        self.model_name = "matthews2016_mantle_ref"
        self.model = model_manager.get_model(self.model_name)
        self.model.set_data_dir(TEMP_TEST_DIR)

    def test(self):
        logger.info("test ...")

        filepath = self.model.get_raster("AgeGrids", 10)
        self.assertTrue(len(filepath) > 0)
        logger.info(filepath)
        self.assertTrue(os.path.isfile(filepath))

        filepaths = self.model.get_rasters("AgeGrids", [10, 11, 12, 13, 14])
        self.assertEqual(len(filepaths), 5)
        logger.info(filepaths)
        for f in filepaths:
            self.assertTrue(os.path.isfile(f))

        self.model.download_time_dependent_rasters("Coastlines", times=[1, 2])

        filepaths = self.model.get_rasters("Topologies", list(range(10)))
        self.assertEqual(len(filepaths), 10)
        logger.info(filepaths)
        for f in filepaths:
            self.assertTrue(os.path.isfile(f))


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(TimeDepRastersTestCase("test"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(TimeDepRastersTestCase))
