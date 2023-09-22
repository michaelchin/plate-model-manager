#!/usr/bin/env python
import glob
import os
import sys
import unittest

sys.path.insert(0, f"{os.path.dirname(__file__)}/../src")
from common import TEMP_TEST_DIR, get_test_logger

from plate_model_manager import download_utils

if __name__ == "__main__":
    logger_name = "test_download_file_main"
else:
    logger_name = __name__

logger = get_test_logger(logger_name)


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
            download_utils.download_file(
                files[file],
                f"{TEMP_TEST_DIR}/test-download-file/{file}/.metadata.json",
                f"{TEMP_TEST_DIR}/test-download-file/{file}",
            )
            file_list = glob.glob(f"{TEMP_TEST_DIR}/test-download-file/{file}/*")

            self.assertTrue(len(file_list) > 0)
            self.assertTrue(
                os.path.isfile(
                    f"{TEMP_TEST_DIR}/test-download-file/{file}/.metadata.json"
                )
            )

    @unittest.skipIf(
        int(os.getenv("TEST_LEVEL", 0)) < 1, "this will download a large volume of data"
    )
    def test_download_large_file(self):
        download_utils.download_file(
            "https://repo.gplates.org/webdav/pmm/present-day-rasters/agegrid.tiff.gz",
            f"{TEMP_TEST_DIR}/test-download-file/.metadata.json",
            f"{TEMP_TEST_DIR}/test-download-file/",
            large_file_hint=True,
        )
        self.assertTrue(
            os.path.isfile(f"{TEMP_TEST_DIR}/test-download-file/agegrid.tiff")
        )


if __name__ == "__main__":
    # use the following code to run a list of tests
    # suite = unittest.TestSuite()
    # suite.addTest(DownloadFileTestCase("test_download_file"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    # use the following code to run all tests in this file
    runner = unittest.TextTestRunner()
    runner.run(unittest.TestLoader().loadTestsFromTestCase(DownloadFileTestCase))
