import glob
import io
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import requests
import utils

model_path = utils.get_model_path(sys.argv, "merdith2021")

info_fp = open(f"{model_path}/info.txt", "w+")
info_fp.write(f"{datetime.now()}\n")

zip_url = "https://earthbyte.org/webdav/ftp/Data_Collections/Merdith_etal_2021_ESR/SM2-Merdith_et_al_1_Ga_reconstruction_v1.2.2"
r = requests.get(
    zip_url,
    allow_redirects=True,
)
info_fp.write(f"Download zip file from {zip_url}\n")
Path(f"{model_path}/download-data").mkdir(parents=True, exist_ok=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/download-data")

# zip topologies
files = glob.glob(f"{model_path}/**/[!shapes_]*.gpml", recursive=True)
files = [f for f in files if "poles" not in f]
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies", log_fp=info_fp)

# zip coastlines
files = glob.glob(f"{model_path}/**/shapes_coastlines*", recursive=True)
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines", log_fp=info_fp)


# zip static polygons
files = glob.glob(f"{model_path}/**/shapes_static_polygons*", recursive=True)
utils.zip_files(
    files, f"{model_path}/StaticPolygons.zip", "StaticPolygons", log_fp=info_fp
)


# zip rotations
files = glob.glob(f"{model_path}/**/*.rot", recursive=True)
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations", log_fp=info_fp)

# zip ContinentalPolygons
files = glob.glob(f"{model_path}/**/shapes_continents.gpml", recursive=True)
utils.zip_files(
    files,
    f"{model_path}/ContinentalPolygons.zip",
    "ContinentalPolygons",
    log_fp=info_fp,
)

# zip Cratons
files = glob.glob(f"{model_path}/**/shapes_cratons_Merdith_et_al.gpml", recursive=True)
utils.zip_files(files, f"{model_path}/Cratons.zip", "Cratons", log_fp=info_fp)

shutil.rmtree(f"{model_path}/download-data")
