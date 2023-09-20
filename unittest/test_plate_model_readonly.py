#!/usr/bin/env python
import os
import sys

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR

from plate_model_manager import PlateModel


def main():
    model = PlateModel("Muller2019", data_dir=TEMP_TEST_DIR, readonly=True)

    print(model.get_avail_layers())

    print(model.get_rotation_model())

    print(model.get_layer("Coastlines"))

    print(model.get_COBs())

    print(model.get_topologies())

    print(model.get_data_dir())


if __name__ == "__main__":
    main()
