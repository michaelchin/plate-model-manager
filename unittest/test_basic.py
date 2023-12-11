#!/usr/bin/env python3

import os
import sys

from common import TEMP_TEST_DIR

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from plate_model_manager import PlateModelManager


def main():
    pm_manager = PlateModelManager()
    model = pm_manager.get_model("Muller2019", data_dir=TEMP_TEST_DIR)
    print(model.get_rotation_model())

    pm_manager = PlateModelManager(model_manifest="../models.json")
    model = pm_manager.get_model()
    print(model.get_rotation_model())


if __name__ == "__main__":
    main()
