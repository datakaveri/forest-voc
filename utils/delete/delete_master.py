import json
import requests
import os
import sys


token = sys.argv[1]

# local
# url = "https://localhost:8080/"
# verify = False


# ext
url = "https://voc.iudx.org.in"
verify = True

headers = {"token": token, "content-type": "application/ld+json"}


if (verify is True):
    r = requests.delete(url,  headers=headers)
    if r.status_code != 203:
        print("Failed")
else:
    r = requests.delete(url, headers=headers, verify=verify)
