import json
import requests
import os
import sys

dirname = "examples"
token = "localauth"


# local
# url = "https://localhost:8080/examples"
# verify = False

# ext
url = "https://agrijson.org/"
verify = True

headers = {"token": token, "content-type": "application/ld+json"}


failed_list = []
print(url);
for filename in os.listdir(dirname):
    with open(dirname + "/" + filename, 'r') as f:
        doc = json.load(f)
        print("Pushing " + filename)
        if (verify is True):
            r = requests.post(url+"/"+filename, data=json.dumps(doc), headers=headers)
            if r.status_code != 201 :
                failed_list.append(filename)
        else:
            r = requests.post(url+"/"+filename, data=json.dumps(doc), headers=headers, verify=verify)
            print(json.dumps(doc))

with open("failed.txt", "w") as f:
    json.dump(failed_list, f)
