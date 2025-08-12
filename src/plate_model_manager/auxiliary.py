import logging
import os
import re
from typing import Union

from .exceptions import ServerUnavailable
from .plate_model import PlateModel
from .plate_model_manager import PlateModelManager
from .zenodo import ZenodoRecord

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


def check_update():
    """Check if new versions of plate models are available on Zenodo.
    Mainly used by Michael Chin to update the PMM server.
    """
    need_update = False
    models = PlateModelManager().models
    for model_name in models:
        logger.info(f"Checking update for model -- {model_name} ...")
        model = models[model_name]
        if isinstance(model, dict) and "URL" in model and "Version" in model:
            record_id = re.findall(r"zenodo.(\d+)", model["URL"])
            version_id = re.findall(r"zenodo.(\d+)", model["Version"])
            if len(record_id) == 1 and len(version_id) == 1:
                # logger.info(record_id[0])
                latest_id = str(ZenodoRecord(record_id[0]).get_latest_version_id())
                if version_id[0] != latest_id:
                    need_update = True
                    logger.info(
                        f"Model ({model_name}) needs update. The latest version ID is: {latest_id}. Your current version ID is : {version_id[0]}."
                    )
    if not need_update:
        logger.info("All models are up-to-date.")
