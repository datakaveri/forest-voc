#!/usr/local/bin/python3
import json
import os
import glob
import copy
import sys

from collections import OrderedDict


#folder_path = sys.argv[1]
#folder_path = "../../base-schemas/properties/"
paths = ["../../base-schemas/properties/",
        "../../data-models/properties/"]


def create_type(folder_path):
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
            obj = json.load(obj_file)
            if "@graph" in obj.keys():
                if isinstance(obj["@graph"][0]["@type"], str):
                    tmp_list = []
                    tmp_list.append(obj["@graph"][0]["@type"])
                    obj["@graph"][0]["@type"] = tmp_list
                    obj_file.seek(0)
                    json.dump(obj, obj_file, indent=4)
                    obj_file.truncate()
            else:
                print("Graph not present in " + filename)

for path in paths:
    create_type(path)
