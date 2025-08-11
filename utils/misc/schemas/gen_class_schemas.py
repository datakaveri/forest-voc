#!/usr/local/bin/python3
import json
import os
import glob
import sys
import copy

from collections import OrderedDict
if not os.path.exists("./class_schemas/"):
    os.makedirs("./class_schemas/")

template = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "<iudx>/NAME",
    "title": "NAME",
    "describes": "comment",
    "type": "object",
    "required": [ "TAGS" ],
    "properties": {
        "NAME": {
            "$ref": "<iudx>/NAME"
        }
    }
}
class_lookup = {}

#filename = "../../../generated/AccessObjectInfoValue.jsonld"
folder_path = "../../../generated/"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    class_name = filename.replace("../../../generated/", "").replace(".jsonld", "")
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
        if "@graph" in obj.keys():
            tmp_dict = {}
            for ob in obj["@graph"]:
                if "rdfs:Class" in ob["@type"]:
                    sch = OrderedDict()
                    sch["$schema"] = template["$schema"]
                    sch["$id"] = ob["@id"].replace("iudx:","<iudx>/")
                    sch["title"] = ob["rdfs:label"]
                    sch["describes"] = ob["rdfs:comment"]
                    sch["type"] = template["type"]
                    try:
                        if ob["iudx:requiredProperties"] is not None:
                            sch["required"] = ob["iudx:requiredProperties"]
                    except KeyError:
                        pass
                if "rdfs:Class" not in ob["@type"]:
                    try:
                        if ob["iudx:domainIncludes"] is not None:
                            inner_dict = {}
                            outer_dict = {}
                            sch["properties"] = {}
                            inner_dict["$ref"] = ob["@id"].replace("iudx:", "<iudx>/")
                            outer_dict[ob["@id"].replace("iudx:", "")] = inner_dict
                            tmp_dict.update(outer_dict)
                    except KeyError:
                        pass
            sch["properties"] = tmp_dict
            class_lookup[class_name] = copy.deepcopy(sch)
        else:
            print("@graph missing in " + filename)
    with open("./class_schemas/" + class_name + ".json", "w+") as wf:
        json.dump(sch, wf, indent=4)
#with open("./class_lookup.json", "w+") as wf:
#    json.dump(class_lookup, wf, indent=4)
