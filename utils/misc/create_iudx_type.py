#!/usr/local/bin/python3
import json
import os
import glob
import sys

from collections import OrderedDict


folder_path = sys.argv[1]
#folder_path = "../../base-schemas/properties/"
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
            new_list = []
            tmp_obj = OrderedDict()
            new_list.append(tmp_obj)
            try:
                tmp_obj["@id"] = obj["@graph"][0]["@id"]
            except KeyError:
                pass
            try:
                tmp_obj["@type"] = obj["@graph"][0]["@type"]
            except KeyError:
                pass
            try:
                tmp_obj["rdfs:comment"] = obj["@graph"][0]["rdfs:comment"]
            except KeyError:
                pass
            try:
                tmp_obj["rdfs:label"] = obj["@graph"][0]["rdfs:label"]
            except KeyError:
                pass
            try:
                tmp_obj["iudx:domainIncludes"] = obj["@graph"][0]["iudx:domainIncludes"]
            except KeyError:
                pass
            try:
                tmp_obj["iudx:rangeIncludes"] = obj["@graph"][0]["iudx:rangeIncludes"]
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["@id"])
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["@type"])
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["rdfs:comment"])
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["rdfs:label"])
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["iudx:domainIncludes"])
            except KeyError:
                pass
            try:
                del(obj["@graph"][0]["iudx:rangeIncludes"])
            except KeyError:
                pass
            new_dict["@graph"] = new_list
            if bool(obj):
                new_dict["@graph"][0].update(obj["@graph"][0])
            for field in new_dict["@graph"]:
                if isinstance(field["@type"], list):
                    iudx_type = [i for i in field["@type"] if "iudx:" in i]
                    if len(iudx_type) == 1:
                        field["@type"] = iudx_type
                    elif len(field["@type"]) == 1:
                        field["@type"] = field["@type"]
                    else:
                        print("Error: Number of @type properties greater than 2 in " + filename)
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()
        else:
            print("@graph missing in " + filename)
