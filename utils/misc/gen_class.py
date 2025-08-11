#!/usr/local/bin/python3
import json
import os
import glob
import copy

from collections import OrderedDict
from distutils.dir_util import copy_tree

""" Paths for ADEX classes and properties."""
from_classes = ["base-schemas/classes/", "data-models/classes/"]
from_properties= ["base-schemas/properties/", "data-models/properties/"]
""" Path of the temporary directory to house all classes."""
classes_path = "/tmp/all_classes/"
""" Path of the temporary directory to house all properties."""
properties_path = "/tmp/all_properties/"
""" Path of the temporary directory to house expanded classes without super class properties."""
tmp_expanded_path = "/tmp/generated/"


""" Directory to house expanded classes with all super class properties."""
if not os.path.exists("generated/"):
    os.makedirs("generated/")
generated_path = "generated/"


def find(element, array):
    for item in array:
        if item['@id'] == element:
            return item

def generate(class_path, property_path):
    """ Generate expanded classes without the properties of the super class.

    This function appends the @graph object to the class_path file's @graph,
    if the class_path file's ID is present either in the domainIncludes or
    rangeIncludes of the property_path file.

    """
    for class_file in glob.glob(os.path.join(class_path, '*.jsonld')):
        domain = class_file.replace(class_path, "")
        domain = domain.replace(".jsonld", "")
        domain = "adex:" + domain
        with open(class_file, "r+") as class_obj:
            new_dict = OrderedDict()
            obj = json.load(class_obj)
            if "@context" in obj.keys():
                new_dict["@context"] = obj["@context"]
                del(obj["@context"])
            else:
                print("@context missing in " + class_file)
            if "@graph" in obj.keys():
                new_dict["@graph"] = obj["@graph"]
                del(obj["@graph"])
            else:
                print("@graph missing in " + class_file)
            for prop_file in glob.glob(os.path.join(property_path, '*.jsonld')):
                with open(prop_file, "r+") as prop_obj:
                    prop = json.load(prop_obj)
                    if "@graph" in prop.keys():
                        try:
                            includes = find(domain, prop["@graph"][0]["adex:domainIncludes"])
                            if includes is not None:
                                new_dict["@graph"].append(prop["@graph"][0])
                        except KeyError:
                            # Uncomment to check filename in which domainIncludes is missing
                            pass
                        try:
                            includes = find(domain, prop["@graph"][0]["adex:rangeIncludes"])
                            if includes is not None:
                                new_dict["@graph"].append(prop["@graph"][0])
                        except KeyError:
                            # Uncomment to check filename in which rangeIncludes is missing
                            pass
                    else:
                        print("@graph missing in " + prop_file)
            os.makedirs(os.path.dirname(tmp_expanded_path), exist_ok=True)
            with open(tmp_expanded_path + domain.replace("adex:", "") + ".jsonld", "w+") as new_file:
                json.dump(new_dict, new_file, indent=4)


def super_class(prop, expanded_dict):
    try:
        if "rdf:" not in prop["rdfs:subClassOf"]["@id"]:
            with open(tmp_expanded_path + prop["rdfs:subClassOf"]["@id"].split(":")[1] + ".jsonld", "r") as super_file:
                super_obj = json.load(super_file)
                for sub_prop in super_obj["@graph"]:
                    expanded_dict["@graph"].append(sub_prop)
                    super_class(sub_prop, expanded_dict)
    except KeyError:
        pass


def generate_expanded():
    """ Generate expanded classes with the properties of the super class.

    This function appends the @graph object of the super class to the-
    @graph of the class, if the class is a sub class of the mentioned super class.

    """
    final_dict = OrderedDict()
    for expanded_file in glob.glob(os.path.join(tmp_expanded_path, '*.jsonld')):
        with open(expanded_file, "r+") as super_obj_file:
            expanded_dict = OrderedDict()
            obj = json.load(super_obj_file)
            if "@context" in obj.keys():
                expanded_dict["@context"] = obj["@context"]
                del(obj["@context"]) 
            else:
                print("@context missing in " + expanded_file)
            if "@graph" in obj.keys():
                expanded_dict["@graph"] = obj["@graph"]
                try:
                    sub_class = obj["@graph"][0]["rdfs:subClassOf"]["@id"]
                    if "rdf:" not in sub_class:
                        with open(tmp_expanded_path + sub_class.split(":")[1] + ".jsonld", "r") as parent_file:
                            parent_obj = json.load(parent_file)
                            for sub_prop in parent_obj["@graph"]:
                                expanded_dict["@graph"].append(sub_prop)
                                super_class(sub_prop, expanded_dict)
                except KeyError:
                    pass
            os.makedirs(os.path.dirname(generated_path), exist_ok=True)
            with open(generated_path + expanded_file.replace(tmp_expanded_path, ""), "w+") as new_file:
                json.dump(expanded_dict, new_file, indent=4)


if __name__=="__main__":
    """ Copy all class objects(base-schemas classes and data-models classes) to one directory."""
    for directory in from_classes:
        copy_tree(directory, classes_path)
    """ Copy all property objects(base-schemas properties and data-models properties) to one directory.""" 
    for directory in from_properties:
        copy_tree(directory, properties_path)
    generate(classes_path, properties_path)
    generate_expanded()
