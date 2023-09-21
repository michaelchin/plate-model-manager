#!/usr/bin/env python
import os
import sys
import time

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR

from plate_model_manager import network_aiohttp, network_requests

test_urls = [
    "https://repo.gplates.org/webdav/pmm/present-day-rasters/topo15-3601x1801.nc.gz",
    "https://repo.gplates.org/webdav/pmm/matthews2016/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_mantle_ref/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_mantle_ref/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_mantle_ref/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_pmag_ref/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_pmag_ref/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/matthews2016_pmag_ref/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/merdith2021/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/merdith2021/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/merdith2021/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/muller2016/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/muller2016/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/muller2016/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/muller2019/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/muller2019/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/muller2019/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/muller2022/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/muller2022/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/muller2022/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/seton2012/Coastlines.zip",
    "https://repo.gplates.org/webdav/pmm/seton2012/StaticPolygons.zip",
    "https://repo.gplates.org/webdav/pmm/seton2012/Rotations.zip",
    "https://repo.gplates.org/webdav/pmm/models.json",
    "https://repo.gplates.org/webdav/pmm/present_day_rasters.json",
]
test_urls += [
    f"https://www.earthbyte.org/webdav/ftp/Data_Collections/Zahirovic_etal_2016_ESR_AgeGrid/jpegs/EarthByte_Zahirovic_etal_2016_ESR_r888_AgeGrid-{i}.jpg"
    for i in range(20)
]

auto_unzip = True


def test_with_for_loop():
    """requests + "for loop" """
    st = time.time()
    spt = time.process_time()

    print("Start test_with_for_loop ... ")

    count = 0
    for url in test_urls:
        network_requests.fetch_file(
            url,
            f"{TEMP_TEST_DIR}/download-with-for-loop/{str(count)}",
            auto_unzip=auto_unzip,
        )
        count += 1

    et = time.time()
    ept = time.process_time()

    print(f"time: {et - st}")
    print(f"process time: {ept - spt}")

    print("End test_with_for_loop ... ")


def test_concurrent_aiohttp():
    """asyncio + aiohttp"""
    st = time.time()
    spt = time.process_time()
    paths = [
        f"{TEMP_TEST_DIR}/download-concurrently-with-aiohttp/{str(i)}"
        for i in range(len(test_urls))
    ]

    print("Start test_concurrent_aiohttp ... ")

    network_aiohttp.fetch_files(
        test_urls,
        paths,
        auto_unzip=auto_unzip,
    )

    et = time.time()
    ept = time.process_time()

    print(f"time: {et - st}")
    print(f"process time: {ept - spt}")

    print("End test_concurrent_aiohttp ... ")


def test_concurrent_executor():
    """requests + ThreadPoolExecutor + asyncio"""
    st = time.time()
    spt = time.process_time()

    paths = [
        f"{TEMP_TEST_DIR}/download-concurrently-with-executor/{i}"
        for i in range(len(test_urls))
    ]

    print("Start test_concurrent_executor ... ")

    network_requests.fetch_files(
        test_urls,
        paths,
        auto_unzip=auto_unzip,
    )

    et = time.time()
    ept = time.process_time()

    print(f"time: {et - st}")
    print(f"process time: {ept - spt}")

    print("End test_concurrent_executor ... ")


if __name__ == "__main__":
    test_with_for_loop()
    test_concurrent_aiohttp()
    test_concurrent_executor()
