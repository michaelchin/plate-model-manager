import io
import os
import shutil
import sys
import zipfile

import requests
import utils

model_path = utils.get_model_path(sys.argv, "cao2020")

r = requests.get("https://zenodo.org/api/records?q=conceptdoi:3854459")
for record in r.json()["hits"]["hits"]:
    print(record["id"])
    print(record["metadata"]["relations"]["version"])

    for file in record["files"]:
        print(file["key"])
        print(file["links"]["self"])
        # download the model zip file
        r = requests.get(
            file["links"]["self"],
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
    files = [
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/NLR_SLOW_CONTINENT_0Ma_1000Ma_NNR.rot",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/1000-410_toy_introversion_simplified.rot",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/410-250_toy_introversion_simplified.rot",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/Global_EB_250-0Ma_GK07_2017_ASM.rot",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/triple_junction_superoceanic_plates.rot",
    ]
    for f in files:
        f_zip.write(f, f"Rotations/{os.path.basename(f)}")

# zip Coastlines
with zipfile.ZipFile(
    f"{model_path}/Coastlines.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/coastline_file_1000_250_new_valid_time.gpml",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/coastline_file_250_0_new_valid_time.gpml",
    ]
    for f in files:
        f_zip.write(f, f"Coastlines/{os.path.basename(f)}")

# zip COBs
with zipfile.ZipFile(
    f"{model_path}/COBs.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    f_zip.write(
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/COBfile_1000_0_Toy_introversion.gpml",
        "COBs/COBfile_1000_0_Toy_introversion.gpml",
    )

# zip Topologies
with zipfile.ZipFile(
    f"{model_path}/Topologies.zip",
    mode="w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as f_zip:
    files = [
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/TopologyBuildingBlocks_AREPS.gpml",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/Toy_introversion_plate_boundaries_1000_410_new_valid_time.gpml",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/Toy_introversion_plate_boundaries_410_250_new_valid_time.gpml",
        f"{model_path}/1000Myr_synthetic_tectonic_reconstructions/Global_EarthByte_Mesozoic-Cenozoic_plate_boundaries_2016_v5.gpml",
    ]
    for f in files:
        f_zip.write(f, f"Topologies/{os.path.basename(f)}")

shutil.rmtree(f"{model_path}/1000Myr_synthetic_tectonic_reconstructions")
shutil.rmtree(f"{model_path}/__MACOSX")

"""
r = requests.get(
    "https://zenodo.org/api/records?q=conceptdoi:3854459&all_versions=true"
)
"""
