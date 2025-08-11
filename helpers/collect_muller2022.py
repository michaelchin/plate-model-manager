import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

from plate_model_manager.zenodo import ZenodoRecord

# https://zenodo.org/doi/10.5281/zenodo.10297173
record = ZenodoRecord(10297173)
latest_id = record.get_latest_version_id()
print(f"The latest version ID is: {latest_id}.")
filenames = record.get_filenames(latest_id)
print(f"The file names in the latest version: {filenames}")
idx = 0
for i in range(len(filenames)):
    if filenames[i].startswith("Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel"):
        idx = i
        break
file_links = record.get_file_links(latest_id)
print(f"The file links in the latest version: {file_links}")

model_path = utils.get_model_path(sys.argv, "muller2022")
zip_path = "Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel"

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
    z.extractall(f"{model_path}/{zip_path}")

# zip Rotations
with zipfile.ZipFile(
    f"{model_path}/Rotations.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_path}/optimisation/1000_0_rotfile_Merdith_etal_opt.rot"
    info_fp.write(f"Zip Rotations:\n")
    info_fp.write(f"\t{f}\n")
    f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip StaticPolygons
with zipfile.ZipFile(
    f"{model_path}/StaticPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_path}/StaticPolygons/shapes_static_polygons_Merdith_etal.gpml"
    info_fp.write(f"Zip StaticPolygons:\n")
    info_fp.write(f"\t{f}\n")
    f_zip.write(f, f"StaticPolygons/{os.path.basename(f)}")

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [f"{model_path}/{zip_path}/Coastlines/shapes_coastlines_Merdith_etal.gpmlz"]
    info_fp.write(f"Zip Coastlines:\n")
    for f in files:
        f_zip.write(f, f"Coastlines/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")

# zip Topologies
with zipfile.ZipFile(
    f"{model_path}/Topologies.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [
        f"{model_path}/{zip_path}/Topologies/1000-410-Convergence.gpml",
        f"{model_path}/{zip_path}/Topologies/1000-410-Divergence.gpml",
        f"{model_path}/{zip_path}/Topologies/1000-410-Topologies.gpml",
        f"{model_path}/{zip_path}/Topologies/250-0_plate_bounds.gpml",
        f"{model_path}/{zip_path}/Topologies/410-250_plate_bounds.gpml",
        f"{model_path}/{zip_path}/Topologies/TopologyBuildingBlocks.gpml",
        f"{model_path}/{zip_path}/Topologies/1000-410-Transforms.gpml",
    ]
    info_fp.write(f"Zip Topologies:\n")
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")

# zip COBs
with zipfile.ZipFile(
    f"{model_path}/COBs.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_path}/COB_Coasts/COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml"
    f_zip.write(
        f,
        f"COBs/{os.path.basename(f)}",
    )
    info_fp.write(f"Zip COBs:\n")
    info_fp.write(f"\t{f}\n")

# zip ContinentalPolygons
with zipfile.ZipFile(
    f"{model_path}/ContinentalPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [f"{model_path}/{zip_path}/Continents/shapes_continents.gpml"]
    info_fp.write(f"Zip ContinentalPolygons:\n")
    for f in files:
        f_zip.write(f, f"ContinentalPolygons/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")

# zip Cratons
with zipfile.ZipFile(
    f"{model_path}/Cratons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [f"{model_path}/{zip_path}/Cratons/shapes_cratons_Merdith_etal.gpml"]
    info_fp.write(f"Zip Cratons:\n")
    for f in files:
        f_zip.write(f, f"Cratons/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")


shutil.rmtree(f"{model_path}/{zip_path}")

info_fp.close()
