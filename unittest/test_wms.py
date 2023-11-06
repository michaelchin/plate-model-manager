#!/usr/bin/env python3

import os
import sys
import unittest

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR, get_test_logger

from plate_model_manager import wms_client

if __name__ == "__main__":
    logger_name = "test_wms_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)


class WMSTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_wms(self):
        wms_client.get_map(
            layers=[
                "gplates:vertical-gravity-gradient",
                "gplates:vgg-hillshade-intensity",
            ],
            styles=["vgg-grey-style", "vgg-hillshade-style"],
        )


# https://geoserver.gplates.org/geoserver/gplates/wms?service=WMS&version=1.1.0&request=GetMap&layers=gplates%3Avertical-gravity-gradient,gplates:vgg-hillshade-intensity&bbox=-180.0%2C-80.0%2C180.0%2C80.0&width=768&height=341&srs=EPSG%3A4326&styles=vgg-grey-style,vgg-hillshade-style&format=application/openlayers

if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(WMSTestCase("test_wms"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(WMSTestCase))
