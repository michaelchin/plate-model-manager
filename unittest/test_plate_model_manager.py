#!/usr/bin/env python

import os
import sys

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from plate_model_manager import PlateModelManager


def main():
    model_manager = PlateModelManager(f"{os.path.dirname(__file__)}/../models.json")
    print(model_manager.get_available_model_names())
    print(model_manager.get_model("Muller2019"))
    print(model_manager.get_model("no-good-model"))

    print("*******************************************************")

    # test remote models.json with URL
    model_manager = PlateModelManager("https://repo.gplates.org/webdav/pmm/models.json")
    print(model_manager.get_available_model_names())
    print(model_manager.get_model("Muller2019"))
    print(model_manager.get_model("no-good-model"))


if __name__ == "__main__":
    main()
