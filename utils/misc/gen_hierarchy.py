#!/usr/local/bin/python3
import json
import os
import glob
import copy
import sys
import subprocess


folder_path = "/tmp/generated/"
#folder_path = "../../generated/"

def graph(obj):
    hierarchy = ""
    if "@graph" in obj.keys():
            graph_obj = copy.deepcopy(obj["@graph"])
            for i in obj["@graph"]:
                typ = i["@type"][0].split(":")
                if typ[1] == "Class":
                    class_name = i["@id"]
                    cname = i["@id"].split(":")
                    cname = "".join(cname)
                    #print("class " + "\"" + class_name + "\"" + " as " + cname + "{", file=text_file) 
                    hierarchy += class_name
                    for j in graph_obj:
                        for prop in j["@type"]:
                            if "Property" in prop:
                                pass
                                #print("\t" + j["@id"], file=text_file)
                            elif "Relationship" in prop:
                                pass
                                #print("\t" + j["@id"], file=text_file)
                    #print("}", file=text_file)
                    try:
                        if "rdf:" in i["rdfs:subClassOf"]["@id"]:
                            spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                            superclass_name = "".join(spclass_name)
                            super_class = i["rdfs:subClassOf"]["@id"]
                            #print("class " + "\"" + i["rdfs:subClassOf"]["@id"] + "\" "+ "as " + superclass_name, file=text_file)
                            hierarchy = i["rdfs:subClassOf"]["@id"] + hierarchy
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                            #print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                        elif "rdf:" not in i["rdfs:subClassOf"]["@id"]:
                            spclass_name = i["rdfs:subClassOf"]["@id"].split(":")
                            superclass_name = "".join(spclass_name)
                            super_class = i["rdfs:subClassOf"]["@id"]
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                with open(folder_path + super_class[1] + ".jsonld", "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj)
                            #print(superclass_name + " --|> " + cname + " : SubClass", file=text_file)
                    except KeyError:
                        pass
                    print(hierarchy, file=text_file)
    else:
        print("@graph missing in " + filename)

if len(sys.argv) > 1:
    if not os.path.exists("../../diagrams/obj_uml_diagram/"):
        os.makedirs("../../diagrams/obj_uml_diagram/")
    obj_markdown_path = "../../diagrams/obj_uml_diagram/"
    filename = sys.argv[1] 
    #filename = /tmp/generated/AccessObjectInfoValue.jsonld" 
    with open(filename, "r+") as obj_file:
         obj = json.load(obj_file)
         markdown_file = obj_markdown_path + filename.replace(folder_path, "").replace(".jsonld", ".txt")
         with open(obj_markdown_path + filename.replace(folder_path, "").replace(".jsonld", ".txt"), "w+") as text_file:
             #print("@startuml\n", file=text_file)
             graph(obj)
             #print("\n@enduml", file=text_file)
         #which_plantuml = ((subprocess.check_output("which plantuml", shell=True)).decode("utf-8")).rstrip()
         #subprocess.call([which_plantuml, markdown_file])
else:
    if not os.path.exists("../../diagrams/class_uml_diagrams/"):
        os.makedirs("../../diagrams/class_uml_diagrams/")
    markdown_path = "../../diagrams/class_uml_diagrams/"
    for filename in glob.glob(os.path.join(folder_path, '*.jsonld')):
        with open(filename, "r+") as obj_file:
             obj = json.load(obj_file)
             markdown_file = markdown_path + filename.replace(folder_path, "").replace(".jsonld", ".txt")
             with open(markdown_path + filename.replace(folder_path, "").replace(".jsonld", ".txt"), "w+") as text_file:
                 #print("@startuml\n", file=text_file)
                 graph(obj)
                 #print("\n@enduml", file=text_file)
             #which_plantuml = ((subprocess.check_output("which plantuml", shell=True)).decode("utf-8")).rstrip()
             #subprocess.call([which_plantuml, markdown_file])
