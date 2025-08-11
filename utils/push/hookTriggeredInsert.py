"""
    This is a script triggered by github webhook to insert schemas into the voc-server.
    Give relative paths to privkey and cert from iudx-voc folder
"""

import json
import requests
import os
import sys
import time


all_classes_folder = "/tmp/all_classes/"
all_properties_folder = "/tmp/all_properties/"
all_examples_folder = "/tmp/all_examples/"
master_context_file = "./adex.jsonld"

schema_folders = [all_classes_folder, all_properties_folder]

token = ""
with open("../config/vocserver.json", "r") as f:
    token = json.load(f)["vocserver.webhookpasswd"]

url = "https://agrijson.org/"


voc_headers = {"token": token, "content-type": "application/ld+json", "accept": "application/ld+json"}



failed_list = []

failed_schemas = []
failed_examples = []


def post_schema(name, path, doc, max_retries=5):

    if max_retries > 0:
        try:
            r = requests.post(url+path+name, data=json.dumps(doc), 
                    headers=voc_headers, timeout=3)
            if r.status_code != 201:
                post_schema(name, path, doc, max_retries=max_retries-1)
            else:
                return 1
        except Exception as e:
            post_schema(name, path, doc, max_retries=max_retries-1)
        return 1
    return 0


for fldr in schema_folders:
    for filename in os.listdir(fldr):
        try:
            with open(fldr + "/" + filename, 'r') as f:
                print("Pushing " + filename)
                doc = json.load(f)
                name = doc["@graph"][0]["@id"][5:]
                status = post_schema(name, "", doc)
                if (status == 0):
                    failed_list.append(name)
        except Exception as e:
            print("Failed inserting " + name)
            failed_list.append(name)
            failed_schemas.append("fldr" + "/" + filename)

for filename in os.listdir(all_examples_folder):
    try:
        with open(all_examples_folder + "/" + filename, 'r') as f:
            print("Pushing " + filename)
            doc = json.load(f)
            status = post_schema(filename, "examples/", doc)
            if status == 0 :
                failed_list.append(filename)
    except Exception as e:
        print("Failed inserting " + filename)
        failed_list.append(filename)

with open(master_context_file, "r") as f:
    master_context = json.load(f)
    print("Pushing master context")
    status = post_schema("", "", master_context)
    if status == 0:
        failed_list.append("master")

print( "Failed inserting - ", failed_list)
with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
