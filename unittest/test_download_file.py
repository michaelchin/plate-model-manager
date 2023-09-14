import sys

sys.path.insert(0, "../src")
from plate_model_manager import download_utils

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
}

for file in files:
    download_utils.download_file(
        files[file],
        f"test-download-file/{file}/.metadata.json",
        f"test-download-file/{file}",
    )
