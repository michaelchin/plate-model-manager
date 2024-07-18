import glob
import io
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

from plate_model_manager.zenodo import ZenodoRecord

# https://zenodo.org/doi/10.5281/zenodo.10526156
record = ZenodoRecord(10526156)
latest_id = record.get_latest_version_id()
print(f"The latest version ID is: {latest_id}.")
filenames = record.get_filenames(latest_id)
print(f"The file names in the latest version: {filenames}")
idx = 0
for i in range(len(filenames)):
    if filenames[i].startswith("Matthews_etal_2016_GPC"):
        idx = i
        break
file_links = record.get_file_links(latest_id)
print(f"The file links in the latest version: {file_links}")

model_path = utils.get_model_path(sys.argv, "matthews2016_mantle_ref")
zip_path = "Matthews_etal_2016_GPC"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = file_links[idx]
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/{zip_path}")

# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/CorrectedModel/Rotations/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
files = glob.glob(
    f"{model_path}/{zip_path}/CorrectedModel/StaticGeometries/StaticPolygons/*.*"
)
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)


# zip Coastlines
files = glob.glob(
    f"{model_path}/{zip_path}/CorrectedModel/StaticGeometries/Coastlines/*.*"
)
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)

# zip ContinentalPolygons
files = glob.glob(
    f"{model_path}/{zip_path}/CorrectedModel/StaticGeometries/ContinentalPolygons/*.*"
)
utils.zip_files(
    files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons", info_fp
)

# zip Topologies
files = glob.glob(f"{model_path}/{zip_path}/CorrectedModel/Topologies/*.gpml")
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


shutil.rmtree(f"{model_path}/{zip_path}")


info_fp.close()
