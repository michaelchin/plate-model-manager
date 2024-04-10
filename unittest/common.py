import logging
import os
from pathlib import Path

TEMP_TEST_DIR = "temp-test-folder"


def get_test_logger(logger_name):
    logger = logging.getLogger(logger_name)
    Path("unittest-logs").mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(f"unittest-logs/{logger_name}.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s \n\n%(message)s\n")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def is_test_installed_module():
    return (
        "PMM_TEST_INSTALLED_MODULE" in os.environ
        and os.environ["PMM_TEST_INSTALLED_MODULE"].lower() == "true"
    )
