import json
import os
import copy
# print(os.getcwd())
# dms = ["FreightManagement", "GhgReport", "Imagery"]
# dms = ["Farmer"]

target_class = input("Enter the name of the floating class you want to update across Schemas-")

example_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../examples'))

""" Fetching the schema of target class"""
with open(example_folder_path+"/ex_"+target_class+"_schema.jsonld", 'r') as file:
    schema_file = json.load(file)
    target_schema = schema_file["schema"]["properties"]
    del target_schema["type"]
    print("target_schema ", target_schema)


def search_file_in_directory(directory, filename):
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def return_expected_type_class(property_name):
    """
    Function returns a list of classes present in rangeIncludes of the jsonld file for the input property passed
    """
    directory_to_search = "../../data-models"
    file_to_find = property_name+".jsonld"

    prop_file_path = search_file_in_directory(directory_to_search, file_to_find)
    with open(prop_file_path, 'r') as file:
        prop_file = json.load(file)
    range_includes_classes = [i["@id"].split(":")[1] for i in prop_file["@graph"][0]["adex:rangeIncludes"]]

    return range_includes_classes

items = os.listdir(example_folder_path)
for i in items:
    if i not in ["ex_ResourceServer.jsonld", "ex_ResourceGroup.jsonld", "ex_Place.jsonld"]:
        if i.split("_")[2] == "schema.jsonld" and i.split("_")[1] != target_class :
            dm = i.split("_")[1]
            print("DataModel >>> ", dm.upper())
    # for dm in dms:
            schema_file_path = example_folder_path+"/ex_"+dm+"_schema.jsonld"
            with open(schema_file_path, 'r') as file:
                data = json.load(file)
                data_prev = copy.deepcopy(data)
                for k1 in data["schema"]["properties"].keys():
                    l1_structured_props = data["schema"]["properties"][k1].get("properties", None)
                    if l1_structured_props != None:
                        range_includes1 = return_expected_type_class(k1)
                        if target_class in range_includes1:
                            print("L1 --- ", k1, " --- ", range_includes1)
                            data["schema"]["properties"][k1]["properties"] = target_schema

                        for k2 in l1_structured_props.keys():
                            l2_structured_props = data["schema"]["properties"][k1]["properties"][k2].get("properties", None)
                            if l2_structured_props != None:
                                range_includes2 = return_expected_type_class(k2)
                                if target_class in range_includes2:
                                    print("L2 --- ", k2, " --- ", range_includes2)
                                    data["schema"]["properties"][k1]["properties"][k2]["properties"] = target_schema

                                for k3 in l2_structured_props.keys():
                                    l3_structured_props = data["schema"]["properties"][k1]["properties"][k2]["properties"][k3].get("properties", None)
                                    if l3_structured_props != None:
                                        range_includes3 = return_expected_type_class(k3)
                                        if target_class in range_includes3:
                                            print("L3 --- ", k3, " --- ", range_includes3)
                                            data["schema"]["properties"][k1]["properties"][k2]["properties"][k3]["properties"] = target_schema

                if data_prev != data:
                    print("Final Schema", data)
                    with open(schema_file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=3)