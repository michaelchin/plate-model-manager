import logging
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, f"{os.path.dirname(__file__)}/../../src")
from plate_model_manager import PlateModel, PlateModelManager

logger = logging.getLogger(__name__)
Path("logs").mkdir(parents=True, exist_ok=True)
fh = logging.FileHandler(f"logs/{__name__}.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s \n\n%(message)s\n")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


class PlateModelTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)

        print(self.logger.level)
        self.logger.info("setup PlateModelTestCase")
        print("setup PlateModelTestCase")

        model_manager = PlateModelManager(
            f"{os.path.dirname(__file__)}/../../models.json"
        )

        # test remote models.json with URL
        # model_manager = plate_model.PlateModelManager(
        #    "https://www.earthbyte.org/webdav/ftp/gplately/models.json"
        # )

        self.model = model_manager.get_model("Muller2019")
        self.model.set_data_dir("temp-test-folder")

    def test_get(self):
        self.logger.warning("testing get ...")

        print(self.model.get_avail_layers())

        print(self.model.get_rotation_model())

        self.logger.info(self.model.get_layer("Coastlines"))

        print(self.model.get_COBs())

        print(self.model.get_topologies())

        print(self.model.get_data_dir())

        print(self.model.get_raster("AgeGrids", 10))

        print(self.model.get_rasters("AgeGrids", [10, 11, 12, 13, 14]))

    def test_download(self):
        self.logger.info("testing download")
        self.model.download_all_layers()

        self.model.download_time_dependent_rasters("AgeGrids", times=[1, 2])
