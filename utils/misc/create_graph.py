#!/usr/local/bin/python3
import json
import os
import glob
import copy
import sys

from collections import OrderedDict


folder_path = sys.argv[1]
#folder_path = "../../base-schemas/properties/"
#filename = "../../base-schemas/properties/name_test.jsonld"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
        if "@graph" not in obj.keys():
            new_dict = OrderedDict()
            new_list = []
            tmp_obj = OrderedDict()
            template = copy.deepcopy(obj)
            del(obj["@context"])
            new_list.append(tmp_obj)
            try:
                tmp_obj["@id"] = obj["@id"]
            except KeyError:
                pass
            try:
                tmp_obj["@type"] = obj["@type"]
            except KeyError:
                pass
            try:
                tmp_obj["rdfs:comment"] = obj["rdfs:comment"]
            except KeyError:
                pass
            try:
                tmp_obj["rdfs:label"] = obj["rdfs:label"]
            except KeyError:
                pass
            try:
                tmp_obj["iudx:domainIncludes"] = obj["iudx:domainIncludes"]
            except KeyError:
                pass
            try:
                tmp_obj["iudx:rangeIncludes"] = obj["iudx:rangeIncludes"]
            except KeyError:
                pass
            try:
                del(obj["@id"])
            except KeyError:
                pass
            try:
                del(obj["@type"])
            except KeyError:
                pass
            try:
                del(obj["rdfs:comment"])
            except KeyError:
                pass
            try:
                del(obj["rdfs:label"])
            except KeyError:
                pass
            try:
                del(obj["iudx:domainIncludes"])
            except KeyError:
                pass
            try:
                del(obj["iudx:rangeIncludes"])
            except KeyError:
                pass
            new_dict["@context"] = template["@context"]
            new_dict["@graph"] = new_list
            if bool(obj):
                new_dict["@graph"][0].update(obj)
            obj_file.seek(0)
            json.dump(new_dict, obj_file, indent=4)
            obj_file.truncate()
        else:
            print("Graph already present in " + filename)
