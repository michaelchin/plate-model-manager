import glob
import io
import os
import shutil
import sys
import zipfile
from pathlib import Path

import requests

if len(sys.argv) >= 2:
    print(sys.argv)
    model_path = f"{sys.argv[1]}/muller2019"
else:
    model_path = "muller2019"

Path(model_path).mkdir(parents=True, exist_ok=True)

# fetch coastlines
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Global_EarthByte_GPlates_PresentDay_Coastlines.gpmlz",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_path}/Coastlines.gpmlz", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_path}/Coastlines.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(f"{model_path}/Coastlines.gpmlz", "Coastlines/Coastlines.gpmlz")

    os.remove(f"{model_path}/Coastlines.gpmlz")

# fetch static polygons
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Global_EarthByte_GPlates_PresentDay_StaticPlatePolygons.gpmlz",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_path}/StaticPolygons.gpmlz", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_path}/StaticPolygons.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(
            f"{model_path}/StaticPolygons.gpmlz", "StaticPolygons/StaticPolygons.gpmlz"
        )

    os.remove(f"{model_path}/StaticPolygons.gpmlz")

# fetch rotations
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Muller2019-Young2019-Cao2020.rot",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_path}/Muller2019-Young2019-Cao2020.rot", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_path}/Rotations.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(
            f"{model_path}/Muller2019-Young2019-Cao2020.rot",
            "Rotations/Muller2019-Young2019-Cao2020.rot",
        )

    os.remove(f"{model_path}/Muller2019-Young2019-Cao2020.rot")

# fetch topologies
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2019_Tectonics/Muller_etal_2019_PlateMotionModel/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics_Updated.zip",
    allow_redirects=True,
)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

with zipfile.ZipFile(
    f"{model_path}/Topologies.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics/*.gpml"
    )
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

# save COBs
with zipfile.ZipFile(
    f"{model_path}/COBs.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f_zip.write(
        f"{model_path}/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics/StaticGeometries/COBLineSegments/Global_EarthByte_GeeK07_COBLineSegments_2019_v1.gpmlz",
        "COBs/Global_EarthByte_GeeK07_COBLineSegments_2019_v1.gpmlz",
    )

# save ContinentalPolygons
with zipfile.ZipFile(
    f"{model_path}/ContinentalPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics/StaticGeometries/ContinentalPolygons/*.*"
    )
    for f in files:
        f_zip.write(f, f"ContinentalPolygons/{os.path.basename(f)}")

shutil.rmtree(f"{model_path}/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics")
