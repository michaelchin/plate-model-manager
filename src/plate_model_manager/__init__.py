# import functions into __init__.py

__version__ = "1.2.0"

import os

from .plate_model import PlateModel
from .plate_model_manager import PlateModelManager
from .present_day_rasters import PresentDayRasterManager
from .utils.misc import disable_stdout_logging, is_debug_mode, turn_on_debug_logging

if is_debug_mode():
    turn_on_debug_logging()

del os
