import abc
import asyncio
import io
import os
from pathlib import Path

from . import misc_utils, unzip_utils


class FileFetcher(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "fetch_file")
            and callable(subclass.fetch_file)
            and hasattr(subclass, "fetch_files")
            and callable(subclass.fetch_files)
            or hasattr(subclass, "fetch_large_file")
            and callable(subclass.fetch_large_file)
            or NotImplemented
        )

    @abc.abstractmethod
    def fetch_file(
        self,
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

        :returns: new etag

        """

        raise NotImplementedError

    @abc.abstractmethod
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
        raise NotImplementedError

    @abc.abstractmethod
    def _run_fetch_large_file(self, loop, url, filesize, data):
        raise NotImplementedError

    def fetch_large_file(
        self,
        url: str,
        filepath: str,
        filesize: int,
        filename: str = None,
        auto_unzip: bool = True,
    ):
        """use multi-thread to fetch a large file.
            LOOK HERE!!!
            Be careful when use this function. You cannot get partial content if the content is gzip encoded.
            So the file might be larger than the one download directly.
            It is useful when downloading large .zip file.
            Warning: this could be slower than single thread download.
            Some firewall sequences these requests to shape network traffic and defeat the purpose of this function completely.

            check the etag and get content-length before calling this function

        :param url: the file url
        :param filepath: location to keep the file
        :param filesize: the size of file (in bytes)
        :param filename: new file name (optional)
        :param auto_unzip: bool flag to indicate if unzip .zip file automatically

        """
        # create folder to keep the file
        if os.path.isfile(filepath):
            raise Exception(
                f"The 'filepath' is in fact a file. The 'filepath' should be a folder path(non-exist is fine). {filepath}"
            )
        Path(filepath).mkdir(parents=True, exist_ok=True)

        # set up concurrent functions
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        data = [io.BytesIO()]

        try:
            self._run_fetch_large_file(loop, url, filesize, data)
        except Exception as e:
            misc_utils.print_error("Failed to fetch large file!")
            raise Exception("Failed to fetch large file!") from e
        finally:
            loop.close()

        data[0].seek(0)
        # save the file
        if auto_unzip:
            try:
                unzip_utils.save_compressed_data(url, data[0], filepath)
            except:
                print("failed to save zip. try save directly")
                data[0].seek(0)
                self._save_file(url, filepath, filename, data[0].read())
        else:
            self._save_file(url, filepath, filename, data[0].read())

        return

    def _save_file(self, url, filepath, filename, data):
        """helper function to save file to hard drive"""

        Path(filepath).mkdir(parents=True, exist_ok=True)
        if not filename:
            filename = url.split("/")[-1]  # use the filename in the url
        if os.path.isfile(f"{filepath}/{filename}"):
            print(f"Warning: overwriting {filename}")
        with open(f"{filepath}/{filename}", "wb+") as of:
            of.write(data)
