import glob
import io
import os
import shutil
import sys
import zipfile

import requests
import utils

model_path = utils.get_model_path(sys.argv, "muller2022")

# download the model zip file
r = requests.get(
    "https://earthbyte.org/webdav/ftp/Data_Collections/Muller_etal_2022_SE/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel.zip",
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
    f = f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/optimisation/1000_0_rotfile_Merdith_et_al_optimised.rot"
    f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip StaticPolygons
utils.fetch_static_polygons(
    "https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MULLER2022/shapes_static_polygons_Merdith_et_al.gpmlz",
    model_path,
    "shapes_static_polygons_Merdith_et_al.gpmlz",
)

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/shapes_coastlines_Merdith_et_al_v2.gpmlz"
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
    files = [
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/1000-410-Convergence_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/1000-410-Divergence_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/1000-410-Topologies_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/250-0_plate_boundaries_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/410-250_plate_boundaries_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/TopologyBuildingBlocks_Merdith_et_al.gpml",
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/1000-410-Transforms_Merdith_et_al.gpml",
    ]
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

# zip COBs
with zipfile.ZipFile(
    f"{model_path}/COBs.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f_zip.write(
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml",
        "COBs/COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml",
    )

# zip ContinentalPolygons
with zipfile.ZipFile(
    f"{model_path}/ContinentalPolygons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/shapes_continents_Merdith_et_al.gpml"
    )
    for f in files:
        f_zip.write(f, f"ContinentalPolygons/{os.path.basename(f)}")

# zip Cratons
with zipfile.ZipFile(
    f"{model_path}/Cratons.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = glob.glob(
        f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel/shapes_cratons_Merdith_et_al.gpml"
    )
    for f in files:
        f_zip.write(f, f"Cratons/{os.path.basename(f)}")


shutil.rmtree(f"{model_path}/Muller_etal_2022_SE_1Ga_Opt_PlateMotionModel")
shutil.rmtree(f"{model_path}/__MACOSX")
