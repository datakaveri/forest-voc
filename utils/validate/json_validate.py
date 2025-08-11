import json
import sys


itemFile = sys.argv[1]

with open(itemFile, "r") as f:
    try:
        item = json.load(f)
    except Exception as e:
        print(e)
        print("Not a valide json item")

""" TODO: Custom schema validation """
