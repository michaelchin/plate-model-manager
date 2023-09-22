#!/usr/bin/env python
import os
import sys
import unittest

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR, get_test_logger

from plate_model_manager import PlateModel, PlateModelManager

if __name__ == "__main__":
    logger_name = "test_plate_model_manager_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)


class PlateModelManagerestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_plate_model_manager(self):
        model_manager = PlateModelManager(f"{os.path.dirname(__file__)}/../models.json")
        model_names = model_manager.get_available_model_names()
        self.assertTrue(len(model_names) > 0)
        logger.info(model_names)

        model = model_manager.get_model("Muller2019")
        self.assertIsInstance(model, PlateModel)
        no_good = model_manager.get_model("no-good-model")
        self.assertIsNone(no_good)

        # test remote models.json with URL
        model_manager = PlateModelManager(
            "https://repo.gplates.org/webdav/pmm/models.json"
        )
        model_names = model_manager.get_available_model_names()
        model_names = model_manager.get_available_model_names()
        self.assertTrue(len(model_names) > 0)
        logger.info(model_names)

        model = model_manager.get_model("Muller2019")
        self.assertIsInstance(model, PlateModel)
        no_good = model_manager.get_model("no-good-model")
        self.assertIsNone(no_good)


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(PlateModelManagerestCase("test_plate_model_manager"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(PlateModelManagerestCase))
