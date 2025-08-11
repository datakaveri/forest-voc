#!/usr/local/bin/python3
import json
import os
import glob
import sys

from collections import OrderedDict


folder_path = sys.argv[1]
#folder_path = "../../base-schemas/classes/"
#folder_path = "../../base-schemas/properties/"
#filename = "../../base-schemas/classes/TimeProperty.jsonld"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
        new_dict = OrderedDict()
        obj = json.load(obj_file)
        if "@context" in obj.keys():
            new_dict["@context"] = obj["@context"]
            del(obj["@context"]) 
        else:
            print("@context missing in " + filename)
        if "@graph" in obj.keys():
            new_dict["@graph"] = obj["@graph"]
            for field in new_dict["@graph"]:
                label = field["@id"].split(":")
                tmp = field["rdfs:label"]
                field["rdfs:label"] = label[1]
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()
        else:
            print("@graph missing in " + filename)
