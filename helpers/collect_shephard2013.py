import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import requests
import utils

from plate_model_manager.zenodo import ZenodoRecord

# https://zenodo.org/doi/10.5281/zenodo.10595888
record = ZenodoRecord(10595888)
latest_id = record.get_latest_version_id()
print(f"The latest version ID is: {latest_id}.")
filenames = record.get_filenames(latest_id)
print(f"The file names in the latest version: {filenames}")
idx = 0
for i in range(len(filenames)):
    if filenames[i].startswith("Shephard_etal_2013_ESR"):
        idx = i
        break
file_links = record.get_file_links(latest_id)
print(f"The file links in the latest version: {file_links}")

model_path = utils.get_model_path(sys.argv, "shephard2013")
zip_path = "Shephard_etal_2013_ESR"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = file_links[idx]
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    Path(model_path).mkdir(parents=True, exist_ok=True)
    z.extractall(f"{model_path}/{zip_path}")


# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/Rotations/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)

# zip StaticPolygons
files = glob.glob(
    f"{model_path}/{zip_path}/StaticPolygons/Shephard_etal_ESR2013_staticpolygons.gpml"
)
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)

# zip Coastlines
files = glob.glob(
    f"{model_path}/{zip_path}/Coastlines/Shephard_etal_ESR2013_Coastlines.gpml"
)
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)

# zip Topologies
files = glob.glob(
    f"{model_path}/{zip_path}/PlateBoundaries/Shephard_etal_ESR2013_platebounds.gpml"
)
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


shutil.rmtree(f"{model_path}/{zip_path}")
