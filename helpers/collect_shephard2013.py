import glob
import io
import os
import shutil
import sys
import zipfile

import requests
import utils

model_path = utils.get_model_path(sys.argv, "shephard2013")

zip_path = "Shephard_etal_2013_ESR"

# download the model zip file
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Shephard_etal_2013_ESR.zip",
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
    f = f"{model_path}/{zip_path}/Shephard_etal_ESR2013_Global_EarthByte_2013.rot"
    f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip StaticPolygons
with zipfile.ZipFile(
    f"{model_path}/StaticPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f = f"{model_path}/{zip_path}/Static_Polygons/Shephard_etal_ESR2013_Global_staticpolygons.gpml"
    f_zip.write(f, f"StaticPolygons/{os.path.basename(f)}")

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/{zip_path}/Coastlines/Shephard_etal_ESR2013_Global_Coastlines_cookiecuttostatic.gpml"
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
    files = glob.glob(
        f"{model_path}/{zip_path}/Plate_Boundaries_and_Topologies/Shephard_etal_ESR2013_Global_EarthByte_2013.gpml"
    )
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")


shutil.rmtree(f"{model_path}/{zip_path}")
os.remove(f"{model_path}/License.txt")
