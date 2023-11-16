import glob
import io
import os
import shutil
import sys
import zipfile

import requests
import utils

model_path = utils.get_model_path(sys.argv, "muller2016")

# download the model zip file
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2016_AREPS/Muller_etal_2016_AREPS_Supplement/Muller_etal_2016_AREPS_Supplement_v1.17.zip",
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
    f = f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Global_EarthByte_230-0Ma_GK07_AREPS.rot"
    f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip StaticPolygons
with zipfile.ZipFile(
    f"{model_path}/StaticPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Shapefiles/StaticPolygons/*"
    )
    for f in files:
        f_zip.write(f, f"StaticPolygons/{os.path.basename(f)}")

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Shapefiles/Coastlines/*"
    )
    for f in files:
        f_zip.write(f, f"Coastlines/{os.path.basename(f)}")

# zip Topologies
with zipfile.ZipFile(
    f"{model_path}/Topologies.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [
        f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Global_EarthByte_230-0Ma_GK07_AREPS_PlateBoundaries.gpml",
        f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Global_EarthByte_230-0Ma_GK07_AREPS_Topology_BuildingBlocks.gpml",
    ]
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

# zip COBs
with zipfile.ZipFile(
    f"{model_path}/COBs.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f_zip.write(
        f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17/Global_EarthByte_230-0Ma_GK07_AREPS_COB_Terranes.gpml",
        "COBs/Global_EarthByte_230-0Ma_GK07_AREPS_COB_Terranes.gpml",
    )

shutil.rmtree(f"{model_path}/Muller_etal_2016_AREPS_Supplement_v1.17")
