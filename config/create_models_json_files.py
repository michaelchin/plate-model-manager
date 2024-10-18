#!/usr/bin/env python3

# use models_v2.json as input
# generate models.json, models_v2_gp.json and models_v2_eb.json
# you should only edit models_v2.json and use this program to generate other files

import json
import re
from functools import cmp_to_key


def compare(first, second):
    first_numbers = re.findall(r"\d+", first)
    second_numbers = re.findall(r"\d+", second)
    if not first_numbers:
        first_numbers = [0]
    if not second_numbers:
        second_numbers = [0]

    if int(first_numbers[0]) > int(second_numbers[0]):
        return -1

    if int(first_numbers[0]) == int(second_numbers[0]):
        return 1 if first > second else -1

    return 1


def sort_cfg_data(data):
    sorted_data = {}
    keys = list(data.keys())
    if "vars" in keys:
        keys.remove("vars")
        sorted_data["vars"] = data["vars"]
    if "default" in keys:
        keys.remove("default")
        sorted_data["default"] = data["default"]
    for key in sorted(keys, key=cmp_to_key(compare)):
        sorted_data[key] = data[key]
    return sorted_data


def generate_cfg(svr_base_url: str, output_file_name, version_1=False):
    assert svr_base_url
    assert output_file_name
    if svr_base_url.endswith("/"):
        svr_base_url = svr_base_url[:-1]
    with open("models_raw_data.json", "r") as f:
        cfg_data = json.load(f)
        cfg_data_str = ""
        if version_1:
            cfg_data.pop("vars", None)
            cfg_data_str = json.dumps(sort_cfg_data(cfg_data), indent=4)
            cfg_data_str = cfg_data_str.replace("@<<SvrBaseURL>>@", svr_base_url)
        else:
            cfg_data["vars"]["SvrBaseURL"] = svr_base_url
            cfg_data_str = json.dumps(sort_cfg_data(cfg_data), indent=4)

        with open(output_file_name, "w") as outf:
            outf.write(cfg_data_str)


generate_cfg("https://repo.gplates.org/webdav/pmm", "models.json", version_1=True)
generate_cfg("https://repo.gplates.org/webdav/pmm", "models_v2.json", version_1=True)
generate_cfg("https://www.earthbyte.org/webdav/pmm", "models_v2_eb.json")
generate_cfg("https://portal.gplates.org/static/pmm", "models_v2_gp.json")
