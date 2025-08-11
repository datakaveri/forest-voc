#!/usr/local/bin/python3
import json
import os
import glob
import copy
import sys

from collections import OrderedDict


folder_path = "../../base-schemas/properties/"
#new_obj_path = "./example_object.json"


def add_obj(new_obj_path):
    with open (new_obj_path, "r") as new_obj_file:
        new_obj = json.load(new_obj_file)
        new_obj_key = list(new_obj.keys())
        new_obj_file.close()
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
            new_dict = OrderedDict()
            obj = json.load(obj_file)
            new_dict["@context"] = obj["@context"]
            new_dict["@graph"] = obj["@graph"]
            for key in new_obj_key:
                new_dict[key] = new_obj[key]
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()


def main():
    add_obj(sys.argv[1])


if __name__ == "__main__":
    main()
