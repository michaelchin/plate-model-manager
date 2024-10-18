import requests
from typing import List, Union, Dict


class ZenodoRecord:
    def __init__(self, conceptrecid):
        self.conceptrecid = conceptrecid
        self._record_url = f"https://zenodo.org/api/records?q=conceptrecid:{conceptrecid}&all_versions=true"
        r = requests.get(self._record_url)
        self.sub_records = r.json()["hits"]["hits"]

    def get_all_versions(self) -> List[Dict]:
        return self.sub_records

    def get_all_version_ids(self) -> List[str]:
        return [record["id"] for record in self.get_all_versions()]

    def get_version(self, id) -> Dict:
        for record in self.get_all_versions():
            if record["id"] == id:
                return record

        raise Exception(
            f"Unable to get version({id}). Check {self._record_url} to find out what is going on."
        )

    def get_latest_version(self) -> Dict:
        for record in self.sub_records:
            if record["metadata"]["relations"]["version"][0]["is_last"] == True:
                return record

        raise Exception(
            f"Unable to find the latest version. Check {self._record_url} to find out what is going on."
        )

    def get_latest_version_id(self) -> str:
        return self.get_latest_version()["id"]

    def get_file_links(self, id) -> List[str]:
        record = self.get_version(id)
        return [file["links"]["self"] for file in record["files"]]

    def get_filenames(self, id) -> List[str]:
        record = self.get_version(id)
        return [file["key"] for file in record["files"]]
