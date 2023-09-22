import logging
from pathlib import Path

TEMP_TEST_DIR = "temp-test-folder"


def get_test_logger(logger_name):
    logger = logging.getLogger(logger_name)
    Path("logs").mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(f"logs/{logger_name}.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s \n\n%(message)s\n")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger
