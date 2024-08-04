import logging
import os
import sys
import warnings

pmm_logger = logging.getLogger("pmm")
pmm_logger.propagate = False
fh = logging.FileHandler(f"pmm.log")
fh.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
)
fh.setFormatter(formatter)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.DEBUG)
pmm_logger.addHandler(fh)
pmm_logger.addHandler(stdout_handler)
pmm_logger.setLevel(logging.INFO)


def turn_on_debug_logging():
    logger = logging.getLogger("pmm")
    logger.setLevel(logging.DEBUG)
    for h in logger.handlers:
        h.setLevel(logging.DEBUG)
    logger.debug("The log level has been set to 'debug'.")


def disable_stdout_logging():
    pmm_logger.removeHandler(stdout_handler)
    print("The logging to stdout has been disabled.")


def my_warningformat(message, category, filename, lineno, line=None):
    return f"{filename}:{lineno}: {category.__name__}: {message}\n"


warnings.formatwarning = my_warningformat


def print_warning(msg):
    # warnings.warn(msg)
    pmm_logger.warning(msg)


def print_error(msg):
    pmm_logger.error(msg)


def is_debug_mode():
    return "PMM_DEBUG" in os.environ and os.environ["PMM_DEBUG"].lower() == "true"
