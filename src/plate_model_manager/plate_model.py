import asyncio
import concurrent.futures
import functools
import glob
import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Union, Dict

from .exceptions import LayerNotFoundInModel
from .utils import download

METADATA_FILENAME = ".metadata.json"

FILE_EXT = [
    "gpml",
    "gpmlz",
    "gpml.gz",
    "dat",
    "pla",
    "shp",
    "geojson",
    "json",
    ".gpkg",
    "gmt",
    "vgp",
]

logger = logging.getLogger("pmm")


class PlateModel:
    """Class to manage a plate model"""

    def __init__(
        self,
        model_name: str,
        model_cfg=None,
        data_dir=".",
        readonly=False,
        timeout=(None, None),
    ):
        """Constructor

        :param model_name: model name
        :param model_cfg: model configuration in JSON format
        :param data_dir: the folder path of the model data
        :param readonly: this will return whatever local folder has. Will not attempt to download data from internet

        """
        self.model_name = model_name.lower()
        self.meta_filename = METADATA_FILENAME
        self._model = model_cfg
        self.readonly = readonly
        self.timeout = timeout

        self.data_dir = data_dir

        self.model_dir = f"{self.data_dir}/{self.model_name}"

        if readonly:
            if not PlateModel.is_model_dir(self.model_dir):
                raise Exception(
                    f"{self.model_dir} must be valid model dir in readonly mode."
                )
            else:
                with open(f"{self.model_dir}/{self.meta_filename}", "r") as f:
                    self._model = json.load(f)

        if not readonly:
            # async and concurrent things
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
            self.loop = asyncio.new_event_loop()
            self.run = functools.partial(self.loop.run_in_executor, self.executor)
            asyncio.set_event_loop(self.loop)

    @property
    def model(self) -> Dict:
        if self._model is not None:
            return self._model
        else:
            raise Exception(
                "The plate model is None. This should not happen. Something Extraordinary must have happened."
            )

    @model.setter
    def model(self, var) -> None:
        self._model = var

    def __getstate__(self):
        attributes = self.__dict__.copy()
        del attributes["executor"]
        del attributes["loop"]
        del attributes["run"]
        return attributes

    def __setstate__(self, state):
        self.__dict__ = state
        if not self.readonly:
            # async and concurrent things
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
            self.loop = asyncio.new_event_loop()
            self.run = functools.partial(self.loop.run_in_executor, self.executor)
            asyncio.set_event_loop(self.loop)

    def __del__(self):
        if not self.readonly:
            try:
                self.loop.close()
            except:
                pass  # ignore the exception when closing the loop if any

    def get_cfg(self):
        return self.model

    def get_model_dir(self):
        if PlateModel.is_model_dir(self.model_dir):
            return self.model_dir
        elif not self.readonly:
            return self.create_model_dir()
        else:
            raise Exception(
                f"The model dir {self.model_dir} is invalid and could not create it (in readonly mode)."
            )

    def get_data_dir(self):
        return self.data_dir

    def set_data_dir(self, new_dir):
        self.data_dir = new_dir
        self.model_dir = f"{self.data_dir}/{self.model_name}/"

    def get_big_time(self):
        return self.model["BigTime"]

    def get_small_time(self):
        return self.model["SmallTime"]

    def get_avail_layers(self):
        """get all available layers in this plate model"""
        if not self.model:
            raise Exception("Fatal: No model configuration found!")
        return list(self.model["Layers"].keys())

    def get_rotation_model(self):
        """return a list of rotation files"""
        if not self.readonly:
            rotation_folder = self.download_layer_files("Rotations")
        else:
            rotation_folder = f"{self.model_dir}/Rotations"
        rotation_files = glob.glob(f"{rotation_folder}/*.rot")
        rotation_files.extend(glob.glob(f"{rotation_folder}/*.grot"))
        # print(rotation_files)
        return rotation_files

    def get_coastlines(
        self, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """return coastlines feature collection"""
        return self.get_layer(
            "Coastlines", return_none_if_not_exist=return_none_if_not_exist
        )

    def get_static_polygons(
        self, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """return StaticPolygons feature collection"""
        return self.get_layer(
            "StaticPolygons", return_none_if_not_exist=return_none_if_not_exist
        )

    def get_continental_polygons(
        self, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """return ContinentalPolygons feature collection"""
        return self.get_layer(
            "ContinentalPolygons", return_none_if_not_exist=return_none_if_not_exist
        )

    def get_topologies(
        self, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """return Topologies feature collection"""
        return self.get_layer(
            "Topologies", return_none_if_not_exist=return_none_if_not_exist
        )

    def get_COBs(
        self, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """return COBs feature collection"""
        return self.get_layer("COBs", return_none_if_not_exist=return_none_if_not_exist)

    def get_layer(
        self, layer_name: str, return_none_if_not_exist: bool = False
    ) -> Union[List[str], None]:
        """get layer files by layer name. raise LayerNotFoundInModel exception to get user's attention by default.
        set `return_none_if_not_exist` if you are sure that your program is OK without this layer.

        :param layer_name: layer name
        :param return_none_if_not_exist: if True, return None when the layer does not exist in the model

        :returns: a list of file names or None if return_none_if_not_exist is True

        :raises LayerNotFoundInModel: if the layer name does not exist in this model

        """
        try:
            if not self.readonly:
                layer_folder = self.download_layer_files(layer_name)
            else:
                layer_folder = f"{self.model_dir}/{layer_name}"
            files = []
            for ext in FILE_EXT:
                files.extend(glob.glob(f"{layer_folder}/*.{ext}"))

            return files
        except LayerNotFoundInModel as e:
            logger.warning(e)
            if return_none_if_not_exist:
                logger.warning(
                    f"The layer({layer_name}) does not exist in model({self.model_name})."
                )
                return None
            else:
                raise e

    def get_raster(self, raster_name: str, time: Union[int, float]) -> str:
        """return a local path for the raster

        :returns: a local path of the raster file
        """

        if not "TimeDepRasters" in self.model:
            raise Exception("No time-dependent rasters found in this model.")
        if not raster_name in self.model["TimeDepRasters"]:
            raise Exception(
                f"Time-dependent rasters ({raster_name}) not found in this model. {self.model['TimeDepRasters']}"
            )
        url = self.model["TimeDepRasters"][raster_name].format(time)

        if not self.readonly:
            self.download_raster(url, f"{self.get_model_dir()}/Rasters/{raster_name}")
        file_name = url.split("/")[-1]
        local_path = f"{self.get_model_dir()}/Rasters/{raster_name}/{file_name}"
        if os.path.isfile(local_path):
            return local_path
        elif self.readonly:
            raise Exception(
                f"You are in readonly mode and the raster {url} has not been downloaded yet."
            )
        else:
            raise Exception(f"Failed to download {url}")

    def get_rasters(
        self, raster_name: str, times: List[Union[int, float]]
    ) -> List[str]:
        """return local paths for the raster files

        :param times: a list of times
        :returns: a list of local paths
        """
        if not "TimeDepRasters" in self.model:
            raise Exception("No time-dependent rasters found in this model.")
        if not raster_name in self.model["TimeDepRasters"]:
            raise Exception(
                f"Time-dependent rasters ({raster_name}) not found in this model. {self.model['TimeDepRasters']}"
            )

        if not self.readonly:
            self.download_time_dependent_rasters(raster_name, times)

        paths = []
        for time in times:
            url = self.model["TimeDepRasters"][raster_name].format(time)
            file_name = url.split("/")[-1]
            local_path = f"{self.get_model_dir()}/Rasters/{raster_name}/{file_name}"
            if os.path.isfile(local_path):
                paths.append(local_path)
            elif self.readonly:
                raise Exception(
                    f"You are in readonly mode and the raster {url} has not been downloaded yet."
                )
            else:
                raise Exception(f"Failed to download {url}")
        return paths

    def create_model_dir(self):
        """create a model folder with a .metadata.json file in it"""
        if self.readonly:
            raise Exception("Unable to create model dir in readonly mode.")
        if not self.model_dir:
            raise Exception(f"Error: model dir is {self.model_dir}")

        # model dir already exists
        if PlateModel.is_model_dir(self.model_dir):
            return self.model_dir

        model_path = self.model_dir
        if os.path.isfile(model_path):
            raise Exception(
                f"Fatal: the model folder {model_path} already exists and is a file!! Remove the file or use another path."
            )

        Path(model_path).mkdir(parents=True, exist_ok=True)

        metadata_file = f"{model_path}/{self.meta_filename}"
        if not os.path.isfile(metadata_file):
            with open(metadata_file, "w+") as f:
                json.dump(self.model, f)

        return model_path

    @staticmethod
    def is_model_dir(folder_path: str):
        """return True if it is a model dir, otherwise False"""
        return os.path.isdir(folder_path) and os.path.isfile(
            f"{folder_path}/.metadata.json"
        )

    def purge(self):
        """remove the model folder and everything inside it"""
        if os.path.isdir(self.model_dir):
            shutil.rmtree(self.model_dir)

    def purge_layer(self, layer_name):
        """remove the layer folder of the given layer name"""
        layer_path = f"{self.model_dir}/{layer_name}"
        if os.path.isdir(layer_path):
            shutil.rmtree(layer_path)

    def purge_time_dependent_rasters(self, raster_name):
        """remove the raster folder of the given raster name"""
        raster_path = f"{self.model_dir}/{raster_name}"
        if os.path.isdir(raster_path):
            shutil.rmtree(raster_path)

    def download_layer_files(self, layer_name):
        """given the layer name, download the layer files.
        The layer files are in a .zip file. download and unzip it.

        :param layer_name: such as "Rotations","Coastlines", "StaticPolygons", "ContinentalPolygons", "Topologies", etc

        :returns: the folder path which contains the layer files

        """
        if self.readonly:
            raise Exception("Unable to download layer files in readonly mode.")

        layer_file_url = self._get_layer_file_url(layer_name)

        model_folder = self.create_model_dir()
        layer_folder = f"{model_folder}/{layer_name}"
        metadata_file = f"{layer_folder}/{self.meta_filename}"

        downloader = download.FileDownloader(
            layer_file_url, metadata_file, model_folder, timeout=self.timeout
        )
        # only re-download when necessary
        if downloader.check_if_file_need_update():
            if os.path.isdir(layer_folder):
                # move the old layer files into "history" folder
                timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                history_dir = f"{model_folder}/history/{layer_name}_{timestamp_str}"
                Path(history_dir).mkdir(parents=True, exist_ok=True)
                shutil.move(layer_folder, history_dir)

            downloader.download_file_and_update_metadata()
        else:
            if downloader.check_if_expire_date_need_update():
                # update the expiry date
                downloader.update_metadata()

            logger.debug(
                f"The local files in {layer_folder} are still good. Will not download again at this moment."
            )

        return layer_folder

    def download_all_layers(self):
        """download all layers. Call download_layer_files() on every layer"""
        if self.readonly:
            raise Exception("Unable to download all layers in readonly mode.")

        async def f():
            tasks = []
            if "Rotations" in self.model:
                tasks.append(self.run(self.download_layer_files, "Rotations"))
            if "Layers" in self.model:
                for layer in self.model["Layers"]:
                    tasks.append(self.run(self.download_layer_files, layer))

            # print(tasks)
            await asyncio.wait(tasks)

        try:
            self.loop.run_until_complete(f())
        except RuntimeError:
            import nest_asyncio

            nest_asyncio.apply()
            self.loop.run_until_complete(f())

    def get_avail_time_dependent_raster_names(self):
        """return the names of all time dependent rasters which have been configurated in this model."""
        if not "TimeDepRasters" in self.model:
            return []
        else:
            return [name for name in self.model["TimeDepRasters"]]

    def download_time_dependent_rasters(self, raster_name, times=None):
        """download time dependent rasters, such agegrids

        :param raster_name: raster name, such as AgeGrids. see the models.json
        :param times: if not given, download from begin to end with 1My interval
        """
        if self.readonly:
            raise Exception(
                "Unable to download time dependent rasters in readonly mode."
            )

        if (
            "TimeDepRasters" in self.model
            and raster_name in self.model["TimeDepRasters"]
        ):

            async def f():
                nonlocal times
                tasks = []

                dst_path = f"{self.get_model_dir()}/Rasters/{raster_name}"
                if not times:
                    times = range(self.model["SmallTime"], self.model["BigTime"] + 1)
                for time in times:
                    tasks.append(
                        self.run(
                            self.download_raster,
                            self.model["TimeDepRasters"][raster_name].format(time),
                            dst_path,
                        )
                    )

                # print(tasks)
                await asyncio.wait(tasks)

            try:
                self.loop.run_until_complete(f())
            except RuntimeError:
                import nest_asyncio

                nest_asyncio.apply()
                self.loop.run_until_complete(f())

        else:
            raise Exception(
                f"Unable to find {raster_name} configuration in this model {self.model_name}."
            )

    def download_raster(self, url, dst_path):
        """download a single raster file from "url" and save the file in "dst_path"
        a metadata file will also be created for the raster file in folder f"{dst_path}/metadata"

        :param url: the url to the raster file
        :param dst_path: the folder path to save the raster file

        """
        if self.readonly:
            raise Exception("Unable to download raster in readonly mode.")
        filename = url.split("/")[-1]
        metadata_folder = f"{dst_path}/.metadata"
        metadata_file = f"{metadata_folder}/{filename}.json"

        downloader = download.FileDownloader(
            url, metadata_file, dst_path, timeout=self.timeout
        )
        # only re-download when necessary
        if downloader.check_if_file_need_update():
            downloader.download_file_and_update_metadata()
        else:
            if downloader.check_if_expire_date_need_update():
                # update the expiry date
                downloader.update_metadata()

            logger.debug(
                f"The local raster file {dst_path}/{filename} is still good. Will not download again at this moment."
            )

    def download_all(self):
        """download everything in this plate model"""
        if self.readonly:
            raise Exception("Unable to download all in readonly mode.")
        self.download_all_layers()
        if "TimeDepRasters" in self.model:
            for raster in self.model["TimeDepRasters"]:
                self.download_time_dependent_rasters(raster)

    def _get_layer_file_url(self, layer_name: str):
        # find the layer file url. two parts. one is the rotation, the other is all other geometry layers
        if layer_name == "Rotations":
            # for Rotations
            return self.model[layer_name]
        elif "Layers" in self.model and layer_name in self.model["Layers"]:
            # for other geometry layers
            return self.model["Layers"][layer_name]
        else:
            logger.debug(f"{json.dumps(self.model, indent=4)}")
            raise LayerNotFoundInModel(
                f"The layer({layer_name}) was not found in model({self.model_name})."
            )
