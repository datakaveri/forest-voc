#!/usr/local/bin/python3
import json
import os
import glob


iudx_classes = os.listdir("../base-schemas/classes")
folder_path = "../base-schemas/properties/"
iudx_classes = os.listdir("../../base-schemas/classes")
folder_path = "../../base-schemas/properties/"
for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
    with open(filename, "r+") as obj_file:
        obj = json.load(obj_file)
    try:
        for item in obj["@graph"]:
            domain_of = item["iudx:domainIncludes"]
            range_of = item["iudx:rangeIncludes"]
            for i in domain_of:
                domain_list = i["@id"].split(":")
                key = domain_list[1] + ".jsonld"
                if key not in iudx_classes:
                    print("Domain " + key + " is not defined in - ",  end="")
                    print(filename)
            for i in range_of:
                if (i["@id"].find("iudx:") != -1):
                    range_list = i["@id"].split(":")
                    key = range_list[1] + ".jsonld"
                    if key not in iudx_classes:
                        print(filename, end="")
                        print("Range " + key + " is not defined in - ", end="")
                        print(filename)
    except KeyError:
        #print("Key not in file - " + filename)
        pass
