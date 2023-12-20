import glob
import io
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "muller2019")
zip_path = "Muller_etal_2019_PlateMotionModel_v2.0_Tectonics_Updated"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2019_Tectonics/Muller_etal_2019_PlateMotionModel/Muller_etal_2019_PlateMotionModel_v2.0_Tectonics_Updated.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/SimplifiedFiles/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
files = glob.glob(
    f"{model_path}/{zip_path}/SimplifiedFiles/Muller_etal_2019_Global_StaticPlatePolygons.gpmlz"
)
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)


# zip Coastlines
files = glob.glob(
    f"{model_path}/{zip_path}/SimplifiedFiles/Muller_etal_2019_Global_Coastlines.gpmlz"
)
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)


# zip Topologies
files = glob.glob(
    f"{model_path}/{zip_path}/SimplifiedFiles/Muller_etal_2019_PlateBoundaries_DeformingNetworks.gpmlz"
)
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


# zip COBs
files = glob.glob(
    f"{model_path}/{zip_path}/StaticGeometries/COBLineSegments/Global_EarthByte_GeeK07_COBLineSegments_2019_v1.gpmlz"
)
utils.zip_files(files, f"{model_path}/COBs.zip", "COBs", info_fp)


# zip ContinentalPolygons
files = glob.glob(f"{model_path}/{zip_path}/StaticGeometries/ContinentalPolygons/*")
utils.zip_files(
    files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons", info_fp
)

shutil.rmtree(f"{model_path}/{zip_path}")

# download the LIPs zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/earthbyte/GPlates/GPlates2.3_GeoData/Individual/IgneousProvinces.zip"
info_fp.write(f"Download the LIPs zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

# zip Whittaker2015LIPs
files = glob.glob(
    f"{model_path}/IgneousProvinces/Whittaker_2015/Whittaker_etal_2015_LIPs.gpmlz"
)
utils.zip_files(
    files, f"{model_path}/Whittaker2015LIPs.zip", "Whittaker2015LIPs", info_fp
)

# zip Johansson_2018_LIPs
files = glob.glob(
    f"{model_path}/IgneousProvinces/Johansson_2018/Johansson_etal_2018_VolcanicProvinces_v2.gpmlz"
)
utils.zip_files(
    files, f"{model_path}/Johansson2018LIPs.zip", "Johansson2018LIPs", info_fp
)

shutil.rmtree(f"{model_path}/IgneousProvinces")


# download the Hotspots zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/earthbyte/GPlates/GPlates2.3_GeoData/Individual/Hotspots.zip"
info_fp.write(f"Download the Hotspots zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

# zip Hotspots
files = glob.glob(f"{model_path}/Hotspots/Hotspots_Compilation_Whittaker_etal.gpmlz")
utils.zip_files(files, f"{model_path}/Hotspots.zip", "Hotspots", info_fp)

shutil.rmtree(f"{model_path}/Hotspots")

# download the SeafloorFabric zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/earthbyte/GPlates/GPlates2.3_GeoData/Individual/SeafloorFabric.zip"
info_fp.write(f"Download the SeafloorFabric zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")

# zip SeafloorFabric
files = glob.glob(f"{model_path}/SeafloorFabric/*.gpmlz")
utils.zip_files(files, f"{model_path}/SeafloorFabric.zip", "SeafloorFabric", info_fp)

shutil.rmtree(f"{model_path}/SeafloorFabric")


info_fp.close()
