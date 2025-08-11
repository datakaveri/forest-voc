import json
import requests
import os
import sys

dirname = sys.argv[1]
token = sys.argv[2]


# local
url = "https://localhost:8080"
verify = False


# ext
# url = "https://voc.iudx.org.in"
# verify = True

headers = {"token": token, "content-type": "application/ld+json"}


failed_list = []
for filename in os.listdir(dirname):
    with open(dirname + "/" + filename, 'r') as f:
        doc = json.load(f)
        name = doc["@graph"][0]["@id"][5:]
        print("Pushing " + name)
        if (verify is True):
            r = requests.post(url+"/"+name, data=json.dumps(doc), headers=headers)
            if r.status_code != 201 :
                failed_list.append(name)
        else:
            r = requests.post(url+"/"+name, data=json.dumps(doc), headers=headers, verify=verify)

with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
