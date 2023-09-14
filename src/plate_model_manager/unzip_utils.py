import bz2
import gzip
import lzma
import shutil
import tarfile
import zipfile


def save_compressed_data(url, data, dst_path):
    """extract files from compressed data

    :param url: URL
    :param data: bytes-like object
    :param dst_path: location to save the files
    """
    # .zip
    if url.endswith(".zip"):
        z = zipfile.ZipFile(data)
        z.extractall(dst_path)
    # .tar.gz or .tgz
    elif url.endswith(".tar.gz") or url.endswith(".tgz"):
        tar = tarfile.open(fileobj=data, mode="r:gz")
        tar.extractall(path=dst_path)
        tar.close()
    # .gz
    elif url.endswith(".gz"):
        fn = url.split("/")[-1][:-3]
        with open(f"{dst_path}/{fn}", "wb+") as f_out:
            with gzip.GzipFile(fileobj=data) as f_in:
                shutil.copyfileobj(f_in, f_out)
    # .tar.bz2 or .tbz2
    elif url.endswith(".tar.bz2") or url.endswith(".tbz2"):
        tar = tarfile.open(fileobj=data, mode="r:bz2")
        tar.extractall(path=dst_path)
        tar.close()
    # .bz2
    elif url.endswith(".bz2"):
        fn = url.split("/")[-1][:-4]
        with open(f"{dst_path}/{fn}", "wb+") as f_out:
            data = bz2.decompress(data.read())
            f_out.write(data)
    # .lzma
    elif url.endswith(".lzma"):
        fn = url.split("/")[-1][:-5]
        with open(f"{dst_path}/{fn}", "wb+") as f_out:
            data = lzma.decompress(data.read())
            f_out.write(data)
    # .tar.xz or .txz
    elif url.endswith(".tar.xz") or url.endswith(".txz"):
        tar = tarfile.open(fileobj=data, mode="r:xz")
        tar.extractall(path=dst_path)
        tar.close()
    # .xz
    elif url.endswith(".xz"):
        fn = url.split("/")[-1][:-3]
        with open(f"{dst_path}/{fn}", "wb+") as f_out:
            data = lzma.decompress(data.read())
            f_out.write(data)
