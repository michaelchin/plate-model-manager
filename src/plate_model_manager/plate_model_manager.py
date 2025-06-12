import json
import logging
import os
import re
from typing import Dict, Union

import requests

from .exceptions import InvalidConfigFile, ServerUnavailable
from .plate_model import PlateModel

logger = logging.getLogger("pmm")


class PlateModelManager:
    """Manage a set of public available plate reconstruction models.
    The model files are hosted on EarthByte servers.
    You need Internet connection to download the files.
    """

    # Load a models.json file and manage plate models.
    # See an example models.json file at PlateModelManager.get_default_repo_url().

    def __init__(self, model_manifest: str = "", timeout=(None, None)):
        """Constructor. Create a :class:`PlateModelManager` instance.

        :param model_manifest: The URL to a ``models.json`` metadata file.
                               Normally you don't need to provide this parameter unless
                               you would like to setup your own plate model server.

        """
        if not model_manifest:
            self.model_manifest = PlateModelManager.get_default_repo_url()
        else:
            self.model_manifest = model_manifest

        self._models = None
        self.timeout = timeout

        if not isinstance(self.model_manifest, str):
            raise InvalidConfigFile(
                f"The model_manifest '{type(self.model_manifest)}' must be a string. It is either a local file path or a http(s) URL."
            )

        # check if the model manifest file is a local file
        if os.path.isfile(self.model_manifest):
            with open(self.model_manifest) as f:
                self._models = json.load(f)
        elif self.model_manifest.startswith(
            "http://"
        ) or self.model_manifest.startswith("https://"):
            # try the http(s) url
            try:
                r = requests.get(self.model_manifest, timeout=timeout)
                if r.status_code != 200:
                    raise InvalidConfigFile(
                        f"Unable to get valid JSON data from '{self.model_manifest}'. Http request return code: {r.status_code}"
                    )
                else:
                    self._models = r.json()

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
            ):
                raise ServerUnavailable(
                    f"Unable to fetch {self.model_manifest}. No network connection, server unavailable or invalid URL!"
                )
            except requests.exceptions.JSONDecodeError:
                raise InvalidConfigFile(
                    f"Unable to get valid JSON data from '{self.model_manifest}'."
                )
        else:
            raise InvalidConfigFile(
                f"The model_manifest '{self.model_manifest}' must be either a local file path or a http(s) URL."
            )

        if "vars" in self.models:
            self._replace_vars_with_values(self.models["vars"], self.models)
            del self.models["vars"]

    @property
    def models(self) -> Dict:
        """The metadata for all the models."""
        if self._models is not None:
            return self._models
        else:
            raise Exception(
                f"No model found. Check the model manifest {self.model_manifest} for errors."
            )

    @models.setter
    def models(self, var) -> None:
        self._models = var

    def _replace_vars_with_values(self, var_dict, json_obj):
        """Replace the variables in `json_obj` with the real values. The variables are defined in `var_dict`."""
        for key, value in json_obj.items():
            if key == "vars":
                continue
            if isinstance(value, dict):
                self._replace_vars_with_values(var_dict, value)
            elif isinstance(value, str):
                matches = re.findall("@<<(.*)>>@", value)
                for m in matches:
                    if m in var_dict:
                        value = value.replace(f"@<<{m}>>@", var_dict[m])
                json_obj[key] = value
            else:
                continue

    def get_model(
        self, model_name: str = "default", data_dir: str = "."
    ) -> Union[PlateModel, None]:
        """Return a :class:`PlateModel` object for a given model name.

        Call :meth:`get_available_model_names()` to see a list of available model names.

        :param model_name: the model name of interest
        :param data_dir: The folder to save the model files.
                         This ``data_dir`` can be changed with :meth:`PlateModel.set_data_dir()` later.

        :returns: a :class:`PlateModel` object or ``None`` if the model name is no good.

        """
        model_name = model_name.lower()
        if model_name in self.models:
            # model name is an alias
            if isinstance(self.models[model_name], str):
                m_name = self.models[model_name]
                if m_name.startswith("@"):
                    m_name = self.models[model_name][1:]

                m = self.get_model(m_name, data_dir=data_dir)
                if m is None:
                    raise Exception(
                        f"Unable to find model {m_name} to resolve an alias. There must be errors in the {self.model_manifest}"
                    )
                else:
                    return PlateModel(
                        model_name, model_cfg=m.get_cfg(), data_dir=data_dir
                    )
            else:
                return PlateModel(
                    model_name, model_cfg=self.models[model_name], data_dir=data_dir
                )
        else:
            logger.warning(f"Model {model_name} is not available.")
            return None

    def get_available_model_names(self):
        """Return the names of available models as a list."""
        return list(self.models.keys())

    @staticmethod
    def get_local_available_model_names(local_dir: str):
        """Return a list of model names in a local folder.

        :param local_dir: The local folder containing models.
        :type local_dir: str
        """
        models = []
        for file in os.listdir(local_dir):
            d = os.path.join(local_dir, file)
            if os.path.isdir(d) and os.path.isfile(f"{d}/.metadata.json"):
                models.append(file)
        return models

    @staticmethod
    def get_default_repo_url():
        """Return the URL to the configuration data of models."""
        default_repo_url_list = [
            "https://repo.gplates.org/webdav/pmm/config/models_v2.json",
            "https://www.earthbyte.org/webdav/pmm/config/models_v2_eb.json",
            "https://portal.gplates.org/static/pmm/config/models_v2_gp.json",
        ]
        for url in default_repo_url_list:
            try:
                response = requests.head(url, timeout=(5, 5))
                if response.status_code == 200:
                    return url
                else:
                    continue
            except:
                continue
        raise ServerUnavailable()

    def download_all_models(self, data_dir: str = "./") -> None:
        """Download all available models into the ``data_dir``.

        :param data_dir: The folder to save the model files.
        :type data_dir: str
        """
        for name in self.get_available_model_names():
            print(f"download {name}")
            model = self.get_model(name)
            if model is not None:
                model.set_data_dir(data_dir)
                model.download_all_layers()
