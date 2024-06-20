import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "muller2022")
zip_path = "Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel_v1.2.2"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")


# download the model zip file
zip_url = "https://earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2022_SE/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel_v1.2.2"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(
    zip_url,
    allow_redirects=True,
)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")


# zip Rotations
with zipfile.ZipFile(
    f"{model_path}/Rotations.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_path}/optimisation/1000_0_rotfile_Merdith_et_al_optimised.rot"
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
    f = f"{model_path}/{zip_path}/shapes_static_polygons_Merdith_et_al.gpml"
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
    files = glob.glob(f"{model_path}/{zip_path}/shapes_coastlines_Merdith_et_al.gpmlz")
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
        f"{model_path}/{zip_path}/1000-410-Convergence.gpml",
        f"{model_path}/{zip_path}/1000-410-Divergence.gpml",
        f"{model_path}/{zip_path}/1000-410-Topologies.gpml",
        f"{model_path}/{zip_path}/250-0_plate_boundaries.gpml",
        f"{model_path}/{zip_path}/410-250_plate_boundaries.gpml",
        f"{model_path}/{zip_path}/TopologyBuildingBlocks.gpml",
        f"{model_path}/{zip_path}/1000-410-Transforms.gpml",
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
    f = f"{model_path}/{zip_path}/COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml"
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
    files = glob.glob(f"{model_path}/{zip_path}/shapes_continents.gpml")
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
    files = glob.glob(f"{model_path}/{zip_path}/shapes_cratons_Merdith_et_al.gpml")
    info_fp.write(f"Zip Cratons:\n")
    for f in files:
        f_zip.write(f, f"Cratons/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")


shutil.rmtree(f"{model_path}/{zip_path}")
shutil.rmtree(f"{model_path}/__MACOSX")

info_fp.close()
