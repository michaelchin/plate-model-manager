import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "cao2023")
zip_path = "1.8Ga_model_submit"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/Data_Collections/Cao_etal_2023/1.8Ga_model_submit.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")


# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
"""
with zipfile.ZipFile(
    f"{model_path}/StaticPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_static_geom_path}/StaticGeometries/StaticPolygons/Clennett_2020_StaticPolygons.gpml"
    info_fp.write(f"Zip StaticPolygons:\n")
    info_fp.write(f"\t{f}\n")
    f_zip.write(f, f"StaticPolygons/{os.path.basename(f)}")
"""

# zip Coastlines
files = glob.glob(f"{model_path}/{zip_path}/shapes_coasts_Cao.gpmlz")
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)


# zip Topologies
files = [
    f"{model_path}/{zip_path}/250-0_plate_boundaries_Merdith_et_al.gpml",
    f"{model_path}/{zip_path}/410-250_plate_boundaries_Merdith_et_al.gpml",
    f"{model_path}/{zip_path}/1000-410-Transforms_Merdith_et_al_Cao.gpml",
    f"{model_path}/{zip_path}/TopologyBuildingBlocks_Merdith_et_al.gpml",
    f"{model_path}/{zip_path}/1000-410-Topologies_Merdith_et_al_Cao.gpml",
    f"{model_path}/{zip_path}/1000-410-Convergence_Merdith_et_al_Cao.gpml",
    f"{model_path}/{zip_path}/1000-410-Divergence_Merdith_et_al_Cao.gpml",
    f"{model_path}/{zip_path}/1800-1000Ma-plate-boundary_new_valid_time_and_subduction_polarity.gpml",
]
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


# zip COBs
files = glob.glob(f"{model_path}/{zip_path}/COBfile_1800_0.gpml")
utils.zip_files(files, f"{model_path}/COBs.zip", "COBs", info_fp)


# zip ContinentalPolygons
files = glob.glob(f"{model_path}/{zip_path}/shapes_continents_Cao.gpmlz")
utils.zip_files(
    files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons", info_fp
)


shutil.rmtree(f"{model_path}/{zip_path}")

info_fp.close()
