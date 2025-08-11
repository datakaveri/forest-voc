import json
import os
from collections import OrderedDict


data_models_dir = "data-models"

excluded = ["utils", "examples", "generated", "diagrams", ".git"]

examples_dir = "examples"

folders = []


# Recursively list out classes and properties paths
output_file = "adex.jsonld"

for (dirpath, dirnames, filenames) in os.walk("./"):

    if (len([dirpath.find(e) for e in excluded if dirpath.find(e)>0])):
        continue

    if(dirpath.find("classes")>0 or dirpath.find("properties")>0 ):
        folders.append(dirpath)





context = OrderedDict()
contextsources = {}
context = {}

contextsources["type"] = "@type"
contextsources["id"] = "@id"
contextsources["@vocab"] = "https://agrijson.org/"

for fldr in folders:
    for fl in os.listdir(fldr):
        with open(os.path.join(fldr, fl), "r") as f:
            try:
                schema = json.load(f)
                contextsources = {**contextsources,
                                  **schema["@context"]}
                context = {**context,
                           **{fl[:-7]: {"@id": "adex:"+fl[:-7]}}}
            except Exception as e:
                print("Class - " + fl[:-7] + " failed")
                print(e)



context.pop("id")
context["id"] = "@id"
context = {**contextsources, **context}
context_output = {"@context": context}

with open(output_file, "w") as f:
    json.dump(context_output, f, indent=4)
