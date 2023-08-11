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


def fetch_file(url, model_path):
    """fetch one file"""
    r = requests.get(
        url,
        allow_redirects=True,
    )
    if r.status_code in [200]:
        file_name = url.split("/")[-1]
        file_path = f"{model_path}/{file_name}"
        with open(file_path, "wb+") as of:
            of.write(r.content)
        return file_path
    else:
        return None


def zip_files(files, zip_filepath, zip_folder):
    """zip a bunch of files"""
    with zipfile.ZipFile(
        zip_filepath,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        for f in files:
            f_zip.write(f, f"{zip_folder}/{os.path.basename(f)}")
