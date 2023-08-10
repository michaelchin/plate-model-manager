import requests
import zipfile, os, io, glob
from pathlib import Path

model_name = "muller2019"
Path(model_name).mkdir(parents=True, exist_ok=True)

# fetch coastlines
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Global_EarthByte_GPlates_PresentDay_Coastlines.gpmlz",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_name}/Coastlines.gpmlz", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_name}/Coastlines.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(f"{model_name}/Coastlines.gpmlz", "Coastlines/Coastlines.gpmlz")

    os.remove(f"{model_name}/Coastlines.gpmlz")


# fetch topologies
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2019_Tectonics/Muller_etal_2019_PlateMotionModel/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics_Updated.zip",
    allow_redirects=True,
)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_name}/")

with zipfile.ZipFile(
    f"{model_name}/Topologies.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_name}/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics/*.gpml"
    )
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

# fetch static polygons
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Global_EarthByte_GPlates_PresentDay_StaticPlatePolygons.gpmlz",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_name}/StaticPolygons.gpmlz", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_name}/StaticPolygons.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(
            f"{model_name}/StaticPolygons.gpmlz", "StaticPolygons/StaticPolygons.gpmlz"
        )

    os.remove(f"{model_name}/StaticPolygons.gpmlz")

# fetch rotations
r = requests.get(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2019/Muller2019-Young2019-Cao2020.rot",
    allow_redirects=True,
)
if r.status_code in [200]:
    with open(f"{model_name}/Muller2019-Young2019-Cao2020.rot", "wb+") as of:
        of.write(r.content)

    with zipfile.ZipFile(
        f"{model_name}/Rotations.zip",
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        f_zip.write(
            f"{model_name}/Muller2019-Young2019-Cao2020.rot",
            "Rotations/Muller2019-Young2019-Cao2020.rot",
        )

    os.remove(f"{model_name}/Muller2019-Young2019-Cao2020.rot")
