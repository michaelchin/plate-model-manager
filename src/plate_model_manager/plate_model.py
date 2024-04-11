import asyncio
import concurrent.futures
import functools
import glob
import json
import logging
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from . import network_requests
from .utils import download, network

METADATA_FILENAME = ".metadata.json"
EXPIRE_HOURS = 12

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

    def __init__(self, model_name: str, model_cfg=None, data_dir=".", readonly=False):
        """Constructor

        :param model_name: model name
        :param model_cfg: model configuration in JSON format
        :param data_dir: the folder path of the model data
        :param readonly: this will return whatever local folder has. Will not attempt to download data from internet

        """
        self.model_name = model_name.lower()
        self.meta_filename = METADATA_FILENAME
        self.model = model_cfg
        self.readonly = readonly

        self.data_dir = data_dir

        self.model_dir = f"{self.data_dir}/{self.model_name}/"

        if readonly:
            if not PlateModel.is_model_dir(self.model_dir):
                raise Exception(
                    f"{self.model_dir} must be valid model dir in readonly mode."
                )
            else:
                with open(f"{self.model_dir}/.metadata.json", "r") as f:
                    self.model = json.load(f)

        if not readonly:
            # async and concurrent things
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
            self.loop = asyncio.new_event_loop()
            self.run = functools.partial(self.loop.run_in_executor, self.executor)
            asyncio.set_event_loop(self.loop)

        # {url:{new-etag:"xxxx", file-size:12345, meta-etag:"uuuuu"}}
        self.etag_and_file_size_cache = {}

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
            self.loop.close()

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

    def get_coastlines(self):
        """return coastlines feature collection"""
        return self.get_layer("Coastlines")

    def get_static_polygons(self):
        """return StaticPolygons feature collection"""
        return self.get_layer("StaticPolygons")

    def get_continental_polygons(self):
        """return ContinentalPolygons feature collection"""
        return self.get_layer("ContinentalPolygons")

    def get_topologies(self):
        """return Topologies feature collection"""
        return self.get_layer("Topologies")

    def get_COBs(self):
        """return COBs feature collection"""
        return self.get_layer("COBs")

    def get_layer(self, layer_name):
        """get layer files by name

        :param layer_name: layer name

        :returns: a list of file names

        """
        if not self.readonly:
            layer_folder = self.download_layer_files(layer_name)
        else:
            layer_folder = f"{self.model_dir}/{layer_name}"
        files = []
        for ext in FILE_EXT:
            files.extend(glob.glob(f"{layer_folder}/*.{ext}"))

        return files

    def get_raster(self, raster_name, time):
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

    def get_rasters(self, raster_name, times):
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

        metadata_file = f"{model_path}/.metadata.json"
        if not os.path.isfile(metadata_file):
            with open(metadata_file, "w+") as f:
                json.dump(self.model, f)

        return model_path

    @staticmethod
    def is_model_dir(folder_path):
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

        # only re-download when necessary
        if self._check_if_layer_files_need_update(layer_name):
            if os.path.isdir(layer_folder):
                # move the old layer files into "history" folder
                timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                history_dir = f"{model_folder}/history/{layer_name}_{timestamp_str}"
                Path(history_dir).mkdir(parents=True, exist_ok=True)
                shutil.move(layer_folder, history_dir)

            if layer_file_url in self.etag_and_file_size_cache:
                file_size = self.etag_and_file_size_cache[layer_file_url]["file-size"]
                meta_etag = self.etag_and_file_size_cache[layer_file_url]["meta-etag"]
            else:
                file_size = None
                meta_etag = None

            if file_size and file_size > 20 * 1000 * 1000:
                new_etag = network_requests.fetch_large_file(
                    layer_file_url,
                    model_folder,
                    filesize=file_size,
                    auto_unzip=True,
                    check_etag=False,
                )
            else:
                new_etag = network_requests.fetch_file(
                    layer_file_url,
                    model_folder,
                    etag=meta_etag,
                    auto_unzip=True,
                )
            # update metadata file
            metadata = {
                "url": layer_file_url,
                "expiry": (datetime.now() + timedelta(hours=EXPIRE_HOURS)).strftime(
                    download.EXPIRY_TIME_FORMAT
                ),
                "etag": new_etag,
            }
            Path("/".join(metadata_file.split("/")[:-1])).mkdir(
                parents=True, exist_ok=True
            )
            with open(metadata_file, "w+") as f:
                json.dump(metadata, f)
        else:
            logger.debug(
                "The local file(s) is/are still good. Will not download again at this moment."
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
                    times = range(self.model["SmallTime"], self.model["BigTime"])
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
        download.download_file(url, metadata_file, dst_path)

    def download_all(self):
        """download everything in this plate model"""
        if self.readonly:
            raise Exception("Unable to download all in readonly mode.")
        self.download_all_layers()
        if "TimeDepRasters" in self.model:
            for raster in self.model["TimeDepRasters"]:
                self.download_time_dependent_rasters(raster)

    def _check_if_layer_files_need_update(self, layer_name: str):
        """check if the layer files need an update(re-download the files)
        return true if "need update", otherwise false

        1. check if the metadata file exists
        2. check if the layer urls match
        3. check expire date
        4. check etag
        """

        layer_folder = f"{self.model_dir}/{layer_name}"
        metadata_file = f"{layer_folder}/{self.meta_filename}"

        #
        # first check if the metadata file exists
        # since metadata file is inside the layer folder, this check will also confirm the existence of the layer folder
        #
        if not os.path.isfile(metadata_file):
            logger.debug(f"the metadata file does not exist, re-download the layer")
            return True

        with open(metadata_file, "r") as f:
            meta = json.load(f)
            layer_file_url = self._get_layer_file_url(layer_name)
            #
            # check if the "url" in the metafile matches the "layer file url"
            #
            if "url" in meta:
                meta_url = meta["url"]
                if meta_url != layer_file_url:
                    logger.debug("the layer url has changed, re-download the layer")
                    return True
            else:
                logger.debug(
                    "no url found in the metafile. to be on the safe side, re-download the layer"
                )
                return True
            #
            # now check the layer file's expiry date
            #
            need_check_etag = False
            if "expiry" in meta:
                try:
                    meta_expiry = meta["expiry"]
                    expiry_date = datetime.strptime(
                        meta_expiry, download.EXPIRY_TIME_FORMAT
                    )
                    now = datetime.now()
                    if now > expiry_date:
                        logger.debug("The file expired. Check etag.")
                        need_check_etag = True  # expired, need to check etag to decide
                    else:
                        # layer file has not expired yet, no need to check update
                        return False
                except ValueError:
                    need_check_etag = (
                        True  # invalid expiry date, need to check etag to decide
                    )
            else:
                need_check_etag = (
                    True  # no expiry date in metafile, need to check etag to make sure
                )

            if need_check_etag:
                if "etag" in meta:
                    meta_etag = meta["etag"]
                    headers = network.get_headers(layer_file_url)
                    file_size = network.get_content_length(headers)
                    new_etag = network.get_etag(headers)

                    # cache the etag and file size. they might be needed later.
                    # primarily performance consideration. avoid network operation as much as possible
                    self.etag_and_file_size_cache = {
                        layer_file_url: {
                            "new-etag": new_etag,
                            "file-size": file_size,
                            "meta-etag": meta_etag,
                        }
                    }

                    if meta_etag == new_etag:
                        logger.debug(f"{meta_etag} -- {new_etag}")
                        return False
                    else:
                        logger.debug("etag has been changed. re-download the layer")
                        return True

                else:
                    logger.debug(
                        "no etag found in the metadata file, to be safe, re-download the layer file"
                    )
                    return True

            logger.debug("This line and below should not be reached!!!!")
            return True

    def _get_layer_file_url(self, layer_name: str):
        # find the layer file url. two parts. one is the rotation, the other is all other geometry layers
        if layer_name == "Rotations":
            # for Rotations
            return self.model[layer_name]
        elif "Layers" in self.model and layer_name in self.model["Layers"]:
            # for other geometry layers
            return self.model["Layers"][layer_name]
        else:
            raise Exception(
                f"The layer ({layer_name}) is not found in the configuration file."
            )
