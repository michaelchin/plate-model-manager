import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "clennett2020_s2013")
zip_path = "Clennett_etal_2020_S2013"
zip_static_geom_path = "Global_Model_WD_Internal_Release_2019_v2_Clennett_NE_Pacific"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/Data_Collections/Clennett_etal_2020_G3/Clennett_etal_2020_S2013.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

# download the model static geometries zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/Data_Collections/Clennett_etal_2020_G3/Global_Model_WD_Internal_Release_2019_v2_Clennett_NE_Pacific.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
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
    files = glob.glob(f"{model_path}/{zip_path}/*.rot")
    info_fp.write(f"Zip Rotations:\n")
    for f in files:
        f_zip.write(f, f"Coastlines/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")


# zip StaticPolygons
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


# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(f"{model_path}/{zip_path}/Clennett_etal_2020_Coastlines.gpml")
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
        f"{model_path}/{zip_path}/Clennett_etal_2020_NAm_boundaries.gpml",
        f"{model_path}/{zip_path}/Clennett_etal_2020_Plates.gpml",
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
    f = f"{model_path}/{zip_static_geom_path}/StaticGeometries/COBLineSegments/Global_EarthByte_GeeK07_COBLineSegments_2019_v1.gpmlz"
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
    files = glob.glob(
        f"{model_path}/{zip_static_geom_path}/StaticGeometries/ContinentalPolygons/*"
    )
    info_fp.write(f"Zip ContinentalPolygons:\n")
    for f in files:
        f_zip.write(f, f"ContinentalPolygons/{os.path.basename(f)}")
        info_fp.write(f"\t{f}\n")


shutil.rmtree(f"{model_path}/{zip_path}")
shutil.rmtree(f"{model_path}/{zip_static_geom_path}")
shutil.rmtree(f"{model_path}/__MACOSX")
os.remove(f"{model_path}/License.txt")

info_fp.close()
