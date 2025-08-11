#!/usr/local/bin/python3
import json
import os
import glob
import sys
import copy

from collections import OrderedDict


folder_path = "../../base-schemas/properties/"


def del_obj(obj_key):
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
            new_dict = OrderedDict()
            obj = json.load(obj_file)
            del(obj[obj_key])
            new_dict["@context"] = obj["@context"]
            all_keys = list(obj.keys())
            for key in all_keys:
                if key != "@context":
                    new_dict[key] = obj[key]
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()


def main():
    del_obj(sys.argv[1])


if __name__ == "__main__":
    main()
