#!/usr/bin/env python3

import os
import sys
import unittest

from common import TEMP_TEST_DIR, get_test_logger, is_test_installed_module

if not is_test_installed_module():
    sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")

import plate_model_manager
from plate_model_manager import PlateModelManager

# plate_model_manager.disable_stdout_logging()

if __name__ == "__main__":
    logger_name = "test_basic_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)

logger.info(plate_model_manager.__file__)


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        pm_manager = PlateModelManager()
        model = pm_manager.get_model("Muller2019", data_dir=TEMP_TEST_DIR)
        logger.info(model.get_rotation_model())

        pm_manager = PlateModelManager(model_manifest="../models.json")
        model = pm_manager.get_model()
        logger.info(model.get_rotation_model())


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(BasicTestCase("test_basic"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(BasicTestCase))
