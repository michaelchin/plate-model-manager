import json
import os
import re

import requests

from .exceptions import InvalidConfigFile, ServerUnavailable
from .plate_model import PlateModel


class PlateModelManager:
    """load a models.json file and manage plate models
    see an example models.json file at PlateModelManager.get_default_repo_url()

    """

    def __init__(self, model_manifest: str = None, timeout=(None, None)):
        """constructor

        :param model_manifest: the path to a models.json file

        """
        if not model_manifest:
            self.model_manifest = PlateModelManager.get_default_repo_url()
        else:
            self.model_manifest = model_manifest

        self.models = None
        self.timeout = timeout

        if not isinstance(self.model_manifest, str):
            raise InvalidConfigFile(
                f"The model_manifest '{type(self.model_manifest)}' must be a string. It is either a local file path or a http(s) URL."
            )

        # check if the model manifest file is a local file
        if os.path.isfile(self.model_manifest):
            with open(self.model_manifest) as f:
                self.models = json.load(f)
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
                    self.models = r.json()

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

    def _replace_vars_with_values(self, var_dict, json_obj):
        """replace the variables in `json_obj` with the real values. the variables are defined in `var_dict`"""
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

    def get_model(self, model_name: str = "default", data_dir: str = "."):
        """return a PlateModel object by model_name

        :param model_name: model name
        :param data_dir: the default data_dir for the model. This dir can be changed with PlateModel.set_data_dir() later.

        :returns: a PlateModel object or none if model name is no good

        """
        model_name = model_name.lower()
        if model_name in self.models:
            # model name is an alias
            if isinstance(self.models[model_name], str):
                m_name = self.models[model_name]
                if m_name.startswith("@"):
                    m_name = self.models[model_name][1:]

                m = self.get_model(m_name, data_dir=data_dir)

                return PlateModel(model_name, model_cfg=m.get_cfg(), data_dir=data_dir)
            else:
                return PlateModel(
                    model_name, model_cfg=self.models[model_name], data_dir=data_dir
                )
        else:
            print(f"Model {model_name} is not available.")
            return None

    def get_available_model_names(self):
        """return the names of available models as a list"""
        return [name for name in self.models]

    @staticmethod
    def get_local_available_model_names(local_dir):
        """list all model names in a local folder"""
        models = []
        for file in os.listdir(local_dir):
            d = os.path.join(local_dir, file)
            if os.path.isdir(d) and os.path.isfile(f"{d}/.metadata.json"):
                models.append(file)
        return models

    @staticmethod
    def get_default_repo_url():
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

    def download_all_models(self, data_dir="./"):
        """download all available models into data_dir"""
        model_names = self.get_available_model_names()
        for name in model_names:
            print(f"download {name}")
            model = self.get_model(name)
            model.set_data_dir(data_dir)
            model.download_all_layers()
