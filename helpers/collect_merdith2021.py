import glob
import io
import shutil
import sys
import zipfile

import requests
import utils

from pathlib import Path

model_path = utils.get_model_path(sys.argv, "merdith2021")

r = requests.get(
    "https://earthbyte.org/webdav/ftp/Data_Collections/Merdith_etal_2021_ESR/SM2-Merdith_et_al_1_Ga_reconstruction_v1.1.zip",
    allow_redirects=True,
)
Path(f"{model_path}/download-data").mkdir(parents=True, exist_ok=True)
if r.status_code in [200]:
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(f"{model_path}/download-data")

# zip topologies
files = glob.glob(f"{model_path}/**/[!shapes_]*.gpml", recursive=True)
files = [f for f in files if "poles" not in f]
utils.zip_files(files, f"{model_path}/Topologies.zip", "Topologies")

# zip coastlines
files = glob.glob(f"{model_path}/**/shapes_coastlines*", recursive=True)
utils.zip_files(files, f"{model_path}/Coastlines.zip", "Coastlines")


# zip static polygons
files = glob.glob(f"{model_path}/**/shapes_static_polygons*", recursive=True)
utils.zip_files(files, f"{model_path}/StaticPolygons.zip", "StaticPolygons")


# zip rotations
files = glob.glob(f"{model_path}/**/*.rot", recursive=True)
utils.zip_files(files, f"{model_path}/Rotations.zip", "Rotations")

# zip ContinentalPolygons
files = glob.glob(f"{model_path}/**/shapes_continents*", recursive=True)
utils.zip_files(files, f"{model_path}/ContinentalPolygons.zip", "ContinentalPolygons")

shutil.rmtree(f"{model_path}/download-data")
