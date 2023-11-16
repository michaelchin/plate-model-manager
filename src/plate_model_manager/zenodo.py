import requests


class ZenodoRecord:
    def __init__(self, conceptrecid):
        self.conceptrecid = conceptrecid
        r = requests.get(
            f"https://zenodo.org/api/records?q=conceptrecid:{conceptrecid}&all_versions=true"
        )
        self.sub_records = r.json()["hits"]["hits"]

    def get_all_versions(self):
        return self.sub_records

    def get_all_version_ids(self):
        return [record["id"] for record in self.get_all_versions()]

    def get_version(self, id):
        for record in self.get_all_versions():
            if record["id"] == id:
                return record

    def get_latest_version(self):
        for record in self.sub_records:
            if record["metadata"]["relations"]["version"][0]["is_last"] == True:
                return record

    def get_latest_version_id(self):
        return self.get_latest_version()["id"]

    def get_file_links(self, id):
        record = self.get_version(id)
        return [file["links"]["self"] for file in record["files"]]

    def get_filenames(self, id):
        record = self.get_version(id)
        return [file["key"] for file in record["files"]]


record = ZenodoRecord(3854459)

print(record.get_all_version_ids())

latest_id = record.get_latest_version_id()
print(latest_id)

filenames = record.get_filenames(latest_id)
print(filenames)

file_links = record.get_file_links(latest_id)
print(file_links)

filenames = record.get_filenames(3854460)
print(filenames)

file_links = record.get_file_links(3854460)
print(file_links)
