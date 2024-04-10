import glob
import json
import os
from hashlib import sha256

import requests

from .network_requests import fetch_file
from .utils import download, misc

DEFAULT_PRESENT_DAY_RASTERS_MANIFEST = (
    "https://repo.gplates.org/webdav/pmm/present_day_rasters.json"
)


class RasterNameNotFound(Exception):
    pass


class PresentDayRasterManager:
    """manage present-day rasters"""

    def __init__(self, raster_manifest=None):
        """constructor

        :param raster_manifest: the path to a present_day_rasters.json file

        """
        if not raster_manifest:
            self.raster_manifest = DEFAULT_PRESENT_DAY_RASTERS_MANIFEST
        else:
            self.raster_manifest = raster_manifest
        self.rasters = None

        self.data_dir = "present-day-rasters"

        # check if the model manifest file is a local file
        if os.path.isfile(self.raster_manifest):
            with open(self.raster_manifest) as f:
                self.rasters = json.load(f)
        elif self.raster_manifest.startswith(
            "http://"
        ) or self.raster_manifest.startswith("https://"):
            # try the http(s) url
            try:
                r = requests.get(self.raster_manifest)
                self.rasters = r.json()

            except requests.exceptions.ConnectionError:
                raise Exception(
                    f"Unable to fetch {self.raster_manifest}. "
                    + "No network connection or invalid URL!"
                )
        else:
            raise Exception(
                f"The model_manifest '{self.raster_manifest}' should be either a local file path or a http(s) URL."
            )

    def set_data_dir(self, folder):
        self.data_dir = folder

    def list_present_day_rasters(self):
        return [name for name in self.rasters]

    def _check_raster_avail(self, _name: str):
        """check if the raster name is in raster configuration"""
        name = _name.lower()
        if not name in self.rasters:
            raise RasterNameNotFound(f"Raster {name} is not found in {self.rasters}.")
        return name

    def is_wms(self, _name: str, check_raster_avail_flag=True):
        """return True if the raster is served by Web Map Service, otherwise False"""
        if check_raster_avail_flag:
            name = self._check_raster_avail(_name)
        else:
            name = _name.lower()
        if (
            isinstance(self.rasters[name], dict)
            and "service" in self.rasters[name]
            and self.rasters[name]["service"] == "WMS"
        ):
            return True
        else:
            return False

    def get_raster(
        self,
        _name: str,
        width=1800,
        height=800,
        bbox=[-180, -80, 180, 80],
    ):
        """download the raster by name. Save the raster in self.data_dir"""
        name = self._check_raster_avail(_name)
        is_wms_flag = self.is_wms(name, check_raster_avail_flag=False)

        if not is_wms_flag:
            download.download_file(
                self.rasters[name],
                f"{self.data_dir}/{name}/.metadata.json",
                f"{self.data_dir}/{name}/",
                large_file_hint=True,
            )
            files = glob.glob(f"{self.data_dir}/{name}/*")
            if len(files) == 0:
                raise Exception(f"Failed to get raster {name}")
            if len(files) > 1:
                misc.print_warning(
                    f"Multiple raster files have been detected.{files}. Return the first one found {files[0]}."
                )
            return files[0]
        else:
            server_url = self.rasters[name]["server_url"]
            version = self.rasters[name]["version"]
            layers = self.rasters[name]["layers"]
            if self.rasters[name]["hillshade_layer"]:
                layers.append(self.rasters[name]["hillshade_layer"])
            styles = self.rasters[name]["styles"]
            if self.rasters[name]["hillshade_style"]:
                styles.append(self.rasters[name]["hillshade_style"])
            format = "image/geotiff"
            url = (
                f"{server_url}/wms?service=WMS&version={version}&request=GetMap&layers={','.join(layers)}"
                + f"&bbox={bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}&width={width}&height={height}&srs=EPSG:4326"
                + f"&styles={','.join(styles)}&format={format}"
            )
            filepath = (
                f"{self.data_dir}/{name}/{sha256(url.encode('utf-8')).hexdigest()}"
            )
            if not os.path.isfile(f"{filepath}/{name}.tiff"):
                fetch_file(
                    url,
                    f"{self.data_dir}/{name}/{sha256(url.encode('utf-8')).hexdigest()}",
                    filename=f"{name}.tiff",
                )
            return f"{filepath}/{name}.tiff"
