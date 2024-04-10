# import functions into __init__.py

__version__ = "1.2.0"

import os

from .misc_utils import disable_stdout_logging, is_debug_mode, turn_on_debug_logging
from .plate_model import PlateModel
from .plate_model_manager import PlateModelManager
from .present_day_rasters import PresentDayRasterManager

if is_debug_mode():
    turn_on_debug_logging()

del misc_utils
del os
