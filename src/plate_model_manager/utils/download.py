import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

from .. import network_requests
from . import network

EXPIRY_TIME_FORMAT = "%Y/%m/%d, %H:%M:%S"
EXPIRE_HOURS = 12

logger = logging.getLogger("pmm")

# {url:{new-etag:"xxxx", file-size:12345, meta-etag:"uuuuu"}}
etag_and_file_size_cache = {}


def check_redownload_need(metadata_file, url):
    """check the metadata file and decide if redownload is necessary

    :param metadata_file: metadata file path
    :param url: url for the target file

    :returns download_flag, etag: a flag indicates if redownload is neccesarry and the old etag in the meta file.
    """
    download_flag = False
    meta_etag = None
    if os.path.isfile(metadata_file):
        with open(metadata_file, "r") as f:
            meta = json.load(f)
            if "url" in meta:
                meta_url = meta["url"]
                if meta_url != url:
                    # if the data url has changed, re-download
                    download_flag = True
            else:
                download_flag = True

            # if the url is the same, now check the expiry date
            if not download_flag:
                if "expiry" in meta:
                    try:
                        meta_expiry = meta["expiry"]
                        expiry_date = datetime.strptime(meta_expiry, EXPIRY_TIME_FORMAT)
                        now = datetime.now()
                        if now > expiry_date:
                            download_flag = True  # expired
                    except ValueError:
                        download_flag = True  # invalid expiry date
                else:
                    download_flag = True  # no expiry date in metafile

                if "etag" in meta:
                    meta_etag = meta["etag"]
    else:
        download_flag = True  # if metadata_file does not exist

    return download_flag, meta_etag


def download_file(
    url, metadata_file, dst_path, expire_hours=EXPIRE_HOURS, large_file_hint=False
):
    """This function will deprecate soon!!!!
    download a file from "url", save the file in "dst_path" and write the metadata

    :param url: the url to the file
    :param metadata_file: the path to the metadata
    :param dst_path: the folder path to save the raster file

    """
    logger.debug(f"downloading {url} into {dst_path} ")
    download_flag, etag = check_redownload_need(metadata_file, url)

    file_size = None
    update_meta = False
    new_etag = etag
    if (download_flag and etag is not None) or large_file_hint:
        # print(f"Checking the etag {url}...")
        # check the file size and etag for large file
        headers = network.get_headers(url)
        file_size = network.get_content_length(headers)
        new_etag = network.get_etag(headers)
        if etag is not None and etag == new_etag:
            download_flag = False
            update_meta = True

    # only redownload when necessary
    if download_flag:
        if file_size and file_size > 20 * 1000 * 1000:
            new_etag = network_requests.fetch_large_file(
                url, dst_path, filesize=file_size, auto_unzip=True, check_etag=False
            )
        else:
            new_etag = network_requests.fetch_file(
                url,
                dst_path,
                etag=etag,
                auto_unzip=True,
            )

    else:
        logger.debug(
            "The local file(s) is/are still good. Will not download again at this moment."
        )

    if etag != new_etag or new_etag is None or update_meta:
        # update metadata file
        metadata = {
            "url": url,
            "expiry": (datetime.now() + timedelta(hours=expire_hours)).strftime(
                EXPIRY_TIME_FORMAT
            ),
            "etag": new_etag,
        }
        Path("/".join(metadata_file.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
        with open(metadata_file, "w+") as f:
            json.dump(metadata, f)


def check_if_file_need_update(file_url: str, meta_filepath: str):
    """check if the file need an update(download/re-download the files)
    return true if "need update", otherwise false

    1. check if the metadata file exists
    2. check if the file urls match
    3. check expire date
    4. check etag
    """

    #
    # first check if the metadata file exists
    # since metadata file is inside the layer folder, this check will also confirm the existence of the layer folder
    #
    if not os.path.isfile(meta_filepath):
        logger.debug(
            f"the metadata file({meta_filepath}) does not exist, need to download the file({file_url})"
        )
        return True

    with open(meta_filepath, "r") as f:
        meta = json.load(f)
        #
        # check if the "url" in the metafile matches the "layer file url"
        #
        if "url" in meta:
            meta_url = meta["url"]
            if meta_url != file_url:
                logger.debug(
                    "the layer url has changed, re-download the file({file_url})"
                )
                return True
        else:
            logger.debug(
                "no url found in the metafile. to be on the safe side, re-download the file({file_url})"
            )
            return True
        #
        # now check the layer file's expiry date
        #
        need_check_etag = False
        if "expiry" in meta:
            try:
                meta_expiry = meta["expiry"]
                expiry_date = datetime.strptime(meta_expiry, EXPIRY_TIME_FORMAT)
                now = datetime.now()
                if now > expiry_date:
                    logger.debug("The file expired. Check etag.")
                    need_check_etag = True  # expired, need to check etag to decide
                else:
                    # layer file has not expired yet, no need to check update
                    return False
            except ValueError:
                need_check_etag = (
                    True  # invalid expiry date, need to check etag to decide
                )
        else:
            need_check_etag = (
                True  # no expiry date in metafile, need to check etag to make sure
            )

        if need_check_etag:
            if "etag" in meta:
                meta_etag = meta["etag"]
                headers = network.get_headers(file_url)
                file_size = network.get_content_length(headers)
                new_etag = network.get_etag(headers)

                # cache the etag and file size. they might be needed later.
                # primarily performance consideration. avoid network operation as much as possible
                etag_and_file_size_cache[file_url] = {
                    "new-etag": new_etag,
                    "file-size": file_size,
                    "meta-etag": meta_etag,
                }

                if meta_etag == new_etag:
                    logger.debug(f"{meta_etag} -- {new_etag}")
                    return False
                else:
                    logger.debug(
                        f"etag has been changed. re-download the file({file_url})"
                    )
                    return True

            else:
                logger.debug(
                    f"no etag found in the metadata file, to be safe, re-download the file({file_url})"
                )
                return True

        logger.debug("This line and below should not be reached!!!!")
        return True


def download_file_and_update_metadata(
    file_url: str, dst_dir: str, metadata_file: str, expire_hours=EXPIRE_HOURS
):
    """download a file from "file_url", save the file in "dst_dir" and update the metadata file

    :param file_url: the url to the file
    :param metadata_file: the path to the metadata file
    :param dst_dir: the destination to save the file

    """
    if file_url in etag_and_file_size_cache:
        file_size = etag_and_file_size_cache[file_url]["file-size"]
        meta_etag = etag_and_file_size_cache[file_url]["meta-etag"]
    else:
        file_size = None
        meta_etag = None

    if file_size and file_size > 20 * 1000 * 1000:
        new_etag = network_requests.fetch_large_file(
            file_url,
            dst_dir,
            filesize=file_size,
            auto_unzip=True,
            check_etag=False,
        )
    else:
        new_etag = network_requests.fetch_file(
            file_url,
            dst_dir,
            etag=meta_etag,
            auto_unzip=True,
        )
    # update metadata file
    metadata = {
        "url": file_url,
        "expiry": (datetime.now() + timedelta(hours=expire_hours)).strftime(
            EXPIRY_TIME_FORMAT
        ),
        "etag": new_etag,
    }
    Path("/".join(metadata_file.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
    with open(metadata_file, "w+") as f:
        json.dump(metadata, f)
