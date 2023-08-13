import os
import zipfile
from pathlib import Path
import tempfile, shutil

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


def fetch_COBs(url, model_path, file_name):
    """fetch COBs"""
    r = requests.get(
        url,
        allow_redirects=True,
    )
    if r.status_code in [200]:
        with open(f"{model_path}/COBs", "wb+") as of:
            of.write(r.content)

        with zipfile.ZipFile(
            f"{model_path}/COBs.zip",
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as f_zip:
            f_zip.write(
                f"{model_path}/COBs",
                f"COBs/{file_name}",
            )

        os.remove(f"{model_path}/COBs")


def fetch_continental_polygons(url, model_path, file_name):
    """fetch continental polygons"""
    r = requests.get(
        url,
        allow_redirects=True,
    )
    if r.status_code in [200]:
        with open(f"{model_path}/continental_polygons", "wb+") as of:
            of.write(r.content)

        with zipfile.ZipFile(
            f"{model_path}/ContinentalPolygons.zip",
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as f_zip:
            f_zip.write(
                f"{model_path}/continental_polygons",
                f"ContinentalPolygons/{file_name}",
            )

        os.remove(f"{model_path}/continental_polygons")


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
    if not len(files) > 0:
        raise Exception("You are trying to zip nothing. We don't allow that.")
    with zipfile.ZipFile(
        zip_filepath,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as f_zip:
        for f in files:
            f_zip.write(f, f"{zip_folder}/{os.path.basename(f)}")


def fetch_and_zip_files(urls, model_path, zip_name):
    """fetch files and zip them"""
    files = []
    tmp_path = tempfile.mkdtemp(dir=model_path)
    for url in urls:
        files.append(
            fetch_file(
                url,
                tmp_path,
            )
        )

    zip_files(
        [f for f in files if f is not None], f"{model_path}/{zip_name}.zip", zip_name
    )

    shutil.rmtree(tmp_path)
