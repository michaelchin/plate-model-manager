import glob
import io
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

from plate_model_manager.zenodo import ZenodoRecord

# https://zenodo.org/records/15233548
record = ZenodoRecord(15233548)
latest_id = record.get_latest_version_id()
print(f"The latest version ID is: {latest_id}.")
filenames = record.get_filenames(latest_id)
print(f"The file names in the latest version: {filenames}")
idx = 0
for i in range(len(filenames)):
    if filenames[i].startswith("Cao_etal_24_1.8Ga_model_mantle_ref_frame"):
        idx = i
        break
file_links = record.get_file_links(latest_id)
print(f"The file links in the latest version: {file_links}")

model_path = utils.get_model_path(sys.argv, "shirmard2025")
zip_path = "Cao_etal_2024_1.8_Ga_mantle_ref_frame"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")


# download the model zip file
zip_url = file_links[idx]
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(
    zip_url,
    allow_redirects=True,
)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    from pathlib import Path

    Path(f"{model_path}").mkdir(parents=True, exist_ok=True)
    z.extractall(f"{model_path}")

# zip Rotations
files = [
    f"{model_path}/{zip_path}/optimisation/1800_1000_rotfile_20240725.rot",
    f"{model_path}/{zip_path}/optimisation/1000_0_rotfile_20240725.rot",
]
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
files = glob.glob(f"{model_path}/{zip_path}/static_polygons.gpmlz")
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)

# zip Coastlines
files = glob.glob(f"{model_path}/{zip_path}/shapes_coasts.gpmlz")
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)


# zip Topologies
files = [
    f"{model_path}/{zip_path}/1000-410-plate-boundaries.gpml",
    f"{model_path}/{zip_path}/1800-1000_plate_boundaries.gpml",
    f"{model_path}/{zip_path}/250-0_plate_boundaries.gpml",
    f"{model_path}/{zip_path}/410-250_plate_boundaries.gpml",
    f"{model_path}/{zip_path}/TopologyBuildingBlocks.gpml",
    f"{model_path}/{zip_path}/1000-410-Convergence.gpml",
    f"{model_path}/{zip_path}/1000-410-Divergence.gpml",
    f"{model_path}/{zip_path}/1000-410-Transforms.gpml",
]
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


# zip COBs
files = glob.glob(f"{model_path}/{zip_path}/COBfile_1800_0.gpml")
utils.zip_files(files, f"{model_path}/COBs.zip", "COBs", info_fp)


# zip ContinentalPolygons
files = glob.glob(f"{model_path}/{zip_path}/shapes_continents.gpmlz")
utils.zip_files(
    files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons", info_fp
)


shutil.rmtree(f"{model_path}/{zip_path}")

info_fp.close()
