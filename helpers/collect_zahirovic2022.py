import glob
import io
import os
import shutil
import sys
import zipfile

import requests
import utils

model_path = utils.get_model_path(sys.argv, "zahirovic2022")
root_path = "Zahirovic_etal_2022_GDJ-ForMichael"

# download the model zip file
r = requests.get(
    "https://repo.gplates.org/webdav/mchin/Zahirovic_etal_2022_GDJ-ForMichael.zip",
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
    f = f"{model_path}/{root_path}/CombinedRotations.rot"
    f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip StaticPolygons
with zipfile.ZipFile(
    f"{model_path}/StaticPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(f"{model_path}/{root_path}/StaticGeometries/StaticPolygons/*")
    for f in files:
        f_zip.write(f, f"StaticPolygons/{os.path.basename(f)}")

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(f"{model_path}/{root_path}/StaticGeometries/Coastlines/*")
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
        f"{model_path}/{root_path}/Plate_Boundaries.gpml",
        f"{model_path}/{root_path}/Feature_Geometries.gpml",
        f"{model_path}/{root_path}/Deforming_Networks_Inactive.gpml",
        f"{model_path}/{root_path}/Deforming_Networks_Active.gpml",
    ]
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

# zip ContinentalPolygons
with zipfile.ZipFile(
    f"{model_path}/ContinentalPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/{root_path}/StaticGeometries/ContinentalPolygons/*.*"
    )
    for f in files:
        f_zip.write(f, f"ContinentalPolygons/{os.path.basename(f)}")

shutil.rmtree(f"{model_path}/{root_path}")
