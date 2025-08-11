import json
import requests
import os
import sys

flname = sys.argv[1]
token = sys.argv[2]


# local
url = "https://localhost:8080/"
verify = False


# ext
# url = "https://voc.iudx.org.in"
# verify = True

headers = {"token": token, "content-type": "application/ld+json", "accept": "application/ld+json"}


failed_list = []
with open(flname, 'r') as f:
    doc = json.load(f)
    print("Sending doc " + json.dumps(doc))
    if (verify is True):
        r = requests.post(url, data=json.dumps(doc), headers=headers)
        print(r.status_code)
        if r.status_code != 201:
            print("Failed")
    else:
        r = requests.post(url, data=json.dumps(doc),
                          headers=headers, verify=verify)
