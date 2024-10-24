import glob
import shutil

import utils

# https://zenodo.org/doi/10.5281/zenodo.10595658
files_path = "z-files"
model_path, info_fp = utils.download_files_from_zenodo(
    "10595658", "zahirovic2014", "Zahirovic_etal_2014_SE", files_path
)

# zip Rotations
files = glob.glob(f"{model_path}/{files_path}/Tectonic_Reconstruction_Model/*.rot")
utils.zip_files_ex(files, model_path, "Rotations", info_fp)

# zip StaticPolygons
files = glob.glob(
    f"{model_path}/{files_path}/Tectonic_Reconstruction_Model/StaticPolygons/*.gpmlz"
)
utils.zip_files_ex(files, model_path, "StaticPolygons", info_fp)

# zip Coastlines
files = glob.glob(
    f"{model_path}/{files_path}/Tectonic_Reconstruction_Model/Coastlines/*.gpmlz"
)
utils.zip_files_ex(files, model_path, "Coastlines", info_fp)


shutil.rmtree(f"{model_path}/{files_path}")
print("Done")
