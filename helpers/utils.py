import os
import zipfile
from pathlib import Path

import requests


def get_model_path(argv, name):
    if len(argv) >= 2:
        print(argv)
        model_path = f"{argv[1]}/{name}"
    else:
        model_path = name

    Path(model_path).mkdir(parents=True, exist_ok=True)
    return model_path


def fetch_coastlines(url, model_path, file_name):
    """fetch coastlines"""
    r = requests.get(
        url,
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
            f_zip.write(
                f"{model_path}/Coastlines.gpmlz",
                f"Coastlines/{file_name}",
            )

        os.remove(f"{model_path}/Coastlines.gpmlz")


def fetch_static_polygons(url, model_path, file_name):
    """fetch static polygons"""
    r = requests.get(
        url,
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
                f"{model_path}/StaticPolygons.gpmlz",
                f"StaticPolygons/{file_name}",
            )

        os.remove(f"{model_path}/StaticPolygons.gpmlz")


def fetch_rotations(url, model_path, file_name):
    """fetch rotations"""
    r = requests.get(
        url,
        allow_redirects=True,
    )
    if r.status_code in [200]:
        with open(f"{model_path}/rotations.rot", "wb+") as of:
            of.write(r.content)

        with zipfile.ZipFile(
            f"{model_path}/Rotations.zip",
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as f_zip:
            f_zip.write(
                f"{model_path}/rotations.rot",
                f"Rotations/{file_name}",
            )

        os.remove(f"{model_path}/rotations.rot")
