#!/usr/bin/env python
import glob
import os
import shutil
import sys
import unittest

from common import TEMP_TEST_DIR, get_test_logger, is_test_installed_module

if not is_test_installed_module():
    sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")

import plate_model_manager
from plate_model_manager.utils import download

# plate_model_manager.disable_stdout_logging()


if __name__ == "__main__":
    logger_name = "test_download_file_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)
logger.info(plate_model_manager.__file__)


class DownloadFileTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_download_file(self):
        files = {
            "test_bz2": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/models.json.bz2",
            "test_lzma": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/models.json.lzma",
            "test_xz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/models.json.xz",
            "test_gz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/models.json.gz",
            "test_tar_gz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.tar.gz",
            "test_tgz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.tgz",
            "test_tar_bz2": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.tar.bz2",
            "test_tar_xz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.tar.xz",
            "test_tbz2": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.tbz2",
            "test_txz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.txz",
            "test_zip": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test.zip",
            "test_bad_zip": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test-bad.zip",
            "test_bad_tar_gz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test-bad.tar.gz",
            "test_bad_xz": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test-bad.xz",
            "test_bad_bz2": "https://repo.gplates.org/webdav/pmm/present-day-rasters/test/test-bad.bz2",
        }

        for file in files:
            if os.path.isdir(f"{TEMP_TEST_DIR}/test-download-file/{file}"):
                shutil.rmtree(f"{TEMP_TEST_DIR}/test-download-file/{file}")
            downloader = download.FileDownloader(
                files[file],
                f"{TEMP_TEST_DIR}/test-download-file/{file}/.metadata.json",
                f"{TEMP_TEST_DIR}/test-download-file/{file}",
            )
            # only re-download when necessary
            if downloader.check_if_file_need_update():
                downloader.download_file_and_update_metadata()
            else:
                logger.info(
                    f"The local file is still good. No need to download {files[file]} again!"
                )

            file_list = glob.glob(f"{TEMP_TEST_DIR}/test-download-file/{file}/*")

            self.assertTrue(len(file_list) > 0)
            self.assertTrue(
                os.path.isfile(
                    f"{TEMP_TEST_DIR}/test-download-file/{file}/.metadata.json"
                )
            )
            self.assertFalse(downloader.check_if_file_need_update())

    @unittest.skipIf(
        int(os.getenv("PMM_TEST_LEVEL", 0)) < 1,
        "this will download a large volume of data",
    )
    def test_download_large_file(self):
        output_filename = f"{TEMP_TEST_DIR}/test-download-file/agegrid.tiff"
        metafile = f"{TEMP_TEST_DIR}/test-download-file/.metadata.json"
        if os.path.isfile(output_filename):
            os.remove(output_filename)
        if os.path.isfile(metafile):
            os.remove(metafile)
        file_url = (
            "https://repo.gplates.org/webdav/pmm/present-day-rasters/agegrid.tiff.gz"
        )
        downloader = download.FileDownloader(
            file_url,
            metafile,
            f"{TEMP_TEST_DIR}/test-download-file/",
            large_file_hint=True,
        )
        if downloader.check_if_file_need_update():
            downloader.download_file_and_update_metadata()
        else:
            logger.info(
                f"The local file is still good. No need to download {file_url} again!"
            )

        self.assertFalse(downloader.check_if_file_need_update())
        self.assertTrue(os.path.isfile(output_filename))
        self.assertTrue(os.path.isfile(metafile))


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(DownloadFileTestCase("test_download_file"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(DownloadFileTestCase))
