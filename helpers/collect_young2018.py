import glob
import io
import os
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "young2018")
zip_path = "Young_etal_2018_GeoscienceFrontiers_GPlatesPlateMotionModel"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = "https://www.earthbyte.org/webdav/ftp/Data_Collections/Young_etal_2018_GeoscienceFrontiers/Young_etal_2018_GeoscienceFrontiers_GPlatesPlateMotionModel.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/")


# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
files = glob.glob(f"{model_path}/{zip_path}/StaticPolygons/*")
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)

# zip Coastlines
files = glob.glob(f"{model_path}/{zip_path}/Coastlines/*")
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)


# zip Topologies
files = [
    f"{model_path}/{zip_path}/Global_Mesozoic-Cenozoic_plate_boundaries_Young_et_al.gpml",
    f"{model_path}/{zip_path}/Global_Paleozoic_plate_boundaries_Young_et_al.gpml",
    f"{model_path}/{zip_path}/TopologyBuildingBlocks_Young_et_al.gpml",
]
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", info_fp)


# zip ContinentalPolygons
files = glob.glob(f"{model_path}/{zip_path}/ContinentalPolygons/*")
utils.zip_files(
    files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons", info_fp
)


shutil.rmtree(f"{model_path}/{zip_path}")
os.remove(f"{model_path}/License.txt")

info_fp.close()
