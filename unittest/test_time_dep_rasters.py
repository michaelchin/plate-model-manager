#!/usr/bin/env python3

import os
import shutil
import sys
import unittest

from common import TEMP_TEST_DIR, get_test_logger, is_test_installed_module

if not is_test_installed_module():
    sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")

import plate_model_manager
from plate_model_manager import PlateModelManager

# plate_model_manager.disable_stdout_logging()

if __name__ == "__main__":
    logger_name = "test_time_dep_rasters_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)
logger.info(plate_model_manager.__file__)


class TimeDepRastersTestCase(unittest.TestCase):
    def setUp(self):
        model_manager = PlateModelManager(
            f"{os.path.dirname(__file__)}/models_test.json"
        )

        # test remote models.json with URL
        # model_manager = plate_model.PlateModelManager(
        #    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
        # )
        self.model_name = "matthews2016_mantle_ref"
        self.model = model_manager.get_model(self.model_name)
        if self.model is not None:
            self.model.set_data_dir(TEMP_TEST_DIR)
        if os.path.isdir(f"{TEMP_TEST_DIR}/matthews2016_mantle_ref/Rasters"):
            shutil.rmtree(f"{TEMP_TEST_DIR}/matthews2016_mantle_ref/Rasters")

    def test(self):
        logger.info("test ...")

        if self.model is None:
            raise Exception("The self.model is None. This should not happen!")

        filepath = self.model.get_raster("AgeGrids", 10)
        self.assertTrue(len(filepath) > 0)
        logger.info(filepath)
        self.assertTrue(os.path.isfile(filepath))

        filepaths = self.model.get_rasters("AgeGrids", [10.0, 11.0, 12, 13, 14])
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
