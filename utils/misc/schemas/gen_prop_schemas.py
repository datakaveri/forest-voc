#!/usr/local/bin/python3
import json
import os
import glob
import sys
import copy

from collections import OrderedDict
if not os.path.exists("./property_schemas/"):
    os.makedirs("./property_schemas/")

template = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "<iudx>/NAME",
    "title": "NAME",
    "describes": "comment",
    "$ref": "<iudx>/Text"
    }
property_lookup = {}

#filename = "../../../base-schemas/properties/address.jsonld"
folder_path = "../../../base-schemas/properties/"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    prop_name = filename.replace("../../../base-schemas/properties/", "").replace(".jsonld", "")
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
        if "@graph" in obj.keys():
            sch = OrderedDict()
            sch["$schema"] = template["$schema"]
            sch["$id"] = obj["@graph"][0]["@id"].replace("iudx:","<iudx>/")
            sch["title"] = obj["@graph"][0]["rdfs:label"]
            sch["describes"] = obj["@graph"][0]["rdfs:comment"]
            try:
                rng = obj["@graph"][0]["iudx:rangeIncludes"]
                if len(rng) > 1:
                    tmp_list = []
                    for item in rng:
                        tmp_dict = {}
                        tmp_dict["$ref"] = item["@id"].replace("iudx:", "<iudx>/")
                        tmp_list.append(tmp_dict)
                    sch["oneOf"] = tmp_list
                elif len(rng) == 1:
                    sch["$ref"] = obj["@graph"][0]["iudx:rangeIncludes"][0]["@id"].replace("iudx:", "<iudx>/")
            except KeyError:
                pass
            property_lookup[prop_name] = copy.deepcopy(sch)
        else:
            print("@graph missing in " + filename)
    with open("./property_schemas/" + prop_name + ".json", "w+") as wf:
        json.dump(sch, wf, indent=4)
#with open("./property_lookup.json", "w+") as wf:
#    json.dump(property_lookup, wf, indent=4)
