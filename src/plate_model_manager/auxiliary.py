import logging
import os
from typing import Union

from .exceptions import ServerUnavailable
from .plate_model import PlateModel
from .plate_model_manager import PlateModelManager

logger = logging.getLogger("pmm")


def get_plate_model(
    model_name: str, data_dir: Union[str, os.PathLike]
) -> Union[PlateModel, None]:
    """Convenient function to create a :class:`PlateModel` instance using best effort.
    First, try to get the plate model with :class:`PlateModelManager`.
    If the servers cannot be reached, try to use the local plate model files which were previously downloaded.

    :param model_name: the plate model name of interest
    :param data_dir: The folder to save the plate model files.

    :returns: a :class:`PlateModel` object or ``None`` if the plate model name is no good.
    """
    try:
        model = PlateModelManager().get_model(model_name, data_dir=data_dir)
    except ServerUnavailable:
        # if unable to connect to the servers, try to use the local files
        model = PlateModel(model_name=model_name, data_dir=data_dir, readonly=True)
        logger.warning(
            "Unable to connect to the servers. Using local files in readonly mode."
        )
    return model
