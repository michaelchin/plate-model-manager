import asyncio
import concurrent.futures
import functools
import io
import os, time
import zipfile
from pathlib import Path

import requests

# This file contains the code to download file(s) from url(s) using "requests" + "asyncio"
# Download files concurrently can improve the performance significantly.
# Download partial content of a large file concurrently may/maynot work depending on the server configuration.


def get_etag(url):
    """return the etag of the given url. The return could be none if the server does not support etag.

    :param url: the url of the file

    """
    return requests.head(url).headers.get("ETag")


def fetch_file(
    url: str,
    filepath: str,
    filename: str = None,
    etag: str = None,
    auto_unzip: bool = True,
):
    """download a file from "url" and save to "filepath"
        You can give a new "filename" for the file.
        If "etag" is given, check if etag has changed. If not changed, do not download again.

    :param url: the url to download file from
    :param filepath: location to keep the file
    :param filename: new file name (optional)
    :param etag: old etag. if the old etag is the same with the one on server, do not download again.
    :param auto_unzip: bool flag to indicate if unzip .zip file automatically

    """

    if etag:
        headers = {"If-None-Match": etag}
    else:
        headers = {}

    if os.path.isfile(filepath):
        raise Exception(
            f"The 'filepath' is in fact a file. The 'filepath' should be a folder path(non-exist is fine). {filepath}"
        )
    Path(filepath).mkdir(parents=True, exist_ok=True)

    r = requests.get(url, allow_redirects=True, headers=headers)
    # print(r.headers)

    if r.status_code == 304:
        print(url)
        print(
            "The file has not been changed since it was downloaded last time. Do nothing and return."
        )
    elif r.status_code == 200:
        if auto_unzip and url.endswith(".zip"):
            # unzip zip file
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(filepath)
        else:
            _save_file(url, filepath, filename, r.content)
    else:
        raise Exception(f"HTTP request failed with code {r.status_code}.")
    new_etag = r.headers.get("ETag").replace(
        "-gzip", ""
    )  # remove the content-encoding awareness thing

    return new_etag


def _fetch_range(url, index: int, chunk_size: int, data: list):
    """get patial content of a file from the server
    Be careful, some server does not support this function.
    And some firewall sequences these requests to shape network traffic and defeat the purpose
    of this function completely. So it might slower than download directly.

    """
    # print(index)
    # st = time.time()
    headers = {
        "Range": f"bytes={index*chunk_size}-{(index+1)*chunk_size-1}",
        "Accept-Encoding": "identity",
    }

    r = requests.get(url, headers=headers)
    data[index].write(r.content)
    # et = time.time()
    # print(f"{index} -- time: {et - st}")


async def _fetch_large_file(
    run, url, file_size: int, data: list, chunk_size=10 * 1000 * 1000
):
    """async implementation of fetch_large_file"""

    num_chunks = file_size // chunk_size + 1
    data_array = [io.BytesIO() for i in range(num_chunks)]
    tasks = [
        run(
            _fetch_range,
            url,
            i,
            chunk_size,
            data_array,
        )
        for i in range(num_chunks)
    ]

    await asyncio.wait(tasks)

    for i in range(num_chunks):
        data_array[i].seek(0)
        data[0].write(data_array[i].read())


def fetch_large_file(
    url: str,
    filepath: str,
    filename: str = None,
    etag: str = None,
    auto_unzip: bool = True,
):
    """use multi-thread to fetch a large file.
        LOOK HERE!!!
        Be careful when use this function. You cannot get partial content if the content is gzip encoded.
        So the file might be larger than the one download directly.
        It is useful when downloading large .zip file.
        Warning: this could be slower than single thread download.
        Some firewall sequences these requests to shape network traffic and defeat the purpose of this function completely.

    :param url: the file url
    :param filepath: location to keep the file
    :param filename: new file name (optional)
    :param etag: old etag. if the old etag is the same with the one on server, do not download again.
    :param auto_unzip: bool flag to indicate if unzip .zip file automatically

    :returns: new etag

    """

    # check file size and etag
    headers = {"Accept-Encoding": "identity"}
    r = requests.head(url, headers=headers)
    # print(r.headers)

    file_size = r.headers.get("Content-Length")
    if not file_size:
        raise Exception(
            "Unable to find the size of the file. Call fetch_file() instead."
        )
    else:
        file_size = int(file_size)

    new_etag = r.headers.get("ETag")
    if new_etag:
        new_etag = new_etag.replace(
            "-gzip", ""
        )  # remove the content-encoding awareness thing
        if new_etag == etag:
            print(url)
            print(
                "The file has not been changed since it was downloaded last time. Do nothing and return."
            )
            return new_etag

    # create folder to keep the file
    if os.path.isfile(filepath):
        raise Exception(
            f"The 'filepath' is in fact a file. The 'filepath' should be a folder path(non-exist is fine). {filepath}"
        )
    Path(filepath).mkdir(parents=True, exist_ok=True)

    # set up concurrent functions
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
    loop = asyncio.new_event_loop()
    run = functools.partial(loop.run_in_executor, executor)

    asyncio.set_event_loop(loop)

    data = [io.BytesIO()]

    try:
        loop.run_until_complete(_fetch_large_file(run, url, file_size, data))
    finally:
        loop.close()

    data[0].seek(0)
    # save the file
    if auto_unzip and url.endswith(".zip"):
        # unzip zip file
        zipfile.ZipFile(data[0]).extractall(filepath)
    else:
        _save_file(url, filepath, filename, data[0].read())

    return new_etag


def _save_file(url, filepath, filename, data):
    """helper function to save file to hard drive"""

    Path(filepath).mkdir(parents=True, exist_ok=True)
    if not filename:
        filename = url.split("/")[-1]  # use the filename in the url
    if os.path.isfile(f"{filepath}/{filename}"):
        print(f"Warning: overwriting {filename}")
    with open(f"{filepath}/{filename}", "wb+") as of:
        of.write(data)


async def _async_fetch_files(
    run,
    urls,
    filepaths,
    filenames=[],
    etags=[],
    auto_unzip: bool = True,
):
    """async implementation of fetch_files function"""
    tasks = []
    for idx, url in enumerate(urls):
        # get filename
        if len(filenames) > idx:
            filename = filenames[idx]
        else:
            filename = None

        # get filepath
        if isinstance(filepaths, str):
            filepath = filepaths
        elif isinstance(filepaths, list) and len(filepaths) > idx:
            filepath = filepaths[idx]
        else:
            raise Exception(
                "The 'filepaths' should be either one string or a list of strings. And the length of the list should be the same with the length of urls. "
            )

        # get etag
        if len(etags) > idx:
            etag = etags[idx]
        else:
            etag = None

        tasks.append(
            run(
                fetch_file,
                url,
                filepath,
                filename,
                etag,
                auto_unzip,
            )
        )
    # print(tasks)
    await asyncio.wait(tasks)


def fetch_files(
    urls,
    filepaths,
    filenames=[],
    etags=[],
    auto_unzip: bool = True,
):
    """fetch multiple files concurrently

    :param urls: the urls to download files from
    :param filepaths: location(s) to keep the files. This can be one path for all files or one path for each file.
    :param filenames: new file names (optional)
    :param etags: old etags. if the old etag is the same with the one on server, do not download again.
    :param auto_unzip: bool flag to indicate if unzip .zip file automatically

    """

    # set up concurrent functions
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)
    loop = asyncio.new_event_loop()
    run = functools.partial(loop.run_in_executor, executor)

    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(
            _async_fetch_files(
                run,
                urls,
                filepaths,
                filenames=filenames,
                etags=etags,
                auto_unzip=auto_unzip,
            )
        )
    finally:
        loop.close()