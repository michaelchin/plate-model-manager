import glob
import io
import shutil
import sys
import zipfile
from datetime import datetime

import requests
import utils

model_path = utils.get_model_path(sys.argv, "torsvikcocks2017")
zip_path = "CEED6"

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

# download the model zip file
zip_url = "https://www.earthdynamics.org/earthhistory/bookdata/CEED6.zip"
info_fp.write(f"Download zip file from {zip_url}\n")
r = requests.get(zip_url, allow_redirects=True, verify=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/{zip_path}")


# zip Rotations
files = glob.glob(f"{model_path}/{zip_path}/*.rot")
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", info_fp)


# zip StaticPolygons
files = glob.glob(f"{model_path}/{zip_path}/CEED6_LAND.*")
files += glob.glob(f"{model_path}/{zip_path}/CEED6_MICROCONTINENTS.*")
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", info_fp)


# zip Coastlines
files = glob.glob(f"{model_path}/{zip_path}/CEED6_LAND.*")
files += glob.glob(f"{model_path}/{zip_path}/CEED6_MICROCONTINENTS.*")
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", info_fp)


shutil.rmtree(f"{model_path}/{zip_path}")

info_fp.close()
