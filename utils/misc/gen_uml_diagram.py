import json
import os, fnmatch
import glob
import copy
import subprocess
from plantuml import PlantUML
import os.path as path
from tkinter import Tk
from tkinter import filedialog
import pytesseract

""" Path to adex-voc."""

Tk().withdraw() 
voc_dir = filedialog.askdirectory(title="Select adex-voc directory")
""" Path to generate the UML diagram."""

Tk().withdraw() 
diagram_path = filedialog.askdirectory(title="Select directory for png")

dup_classes = []
dup_property = []
ct = 1
dict = {}
bg_color = "#F6EEE0"
def find_name(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_id(graph_obj):
    for j in graph_obj:
        for prop in j["@type"]:
            if "Property" in prop:
                print("\t" + j["@id"], file=text_file)
            elif "Relationship" in prop:
                print("\t" + j["@id"], file=text_file)
    print("}", file=text_file)

def graph(obj,cl_dir):
    """ Generate PlantUML text.
    This function generates a text file from the classes,
    which is used by plantuml to generate the UML Ontology diagram for ADEX.

    The cl_dir is the directory of data-type classes in the ADEX voc that needs to be ignored which is not the actual floating class.
    """
    global ct
    global dict
    
    try:
        if "@graph" in obj.keys():
            graph_obj = copy.deepcopy(obj["@graph"])
            for i in obj["@graph"]:
                if i["@type"][0].split(":")[1] == "Class":
                    class_name = i["@id"]
                    cname = i["@id"].split(":")
                    cname = "".join(cname)
                    if class_name not in dup_classes:
                        dup_classes.append(class_name)
                        data_type_dir  = cl_dir.split("/")[-2]
                        
                        if 'rdfs:subClassOf' not in  i and data_type_dir != "data-types":
                            if i['rdfs:label'] != "Thing":
                                print("class " + "\"" + class_name +  f"<sup>{ct}</sup>" + "\"" + " as " + class_name + f" {bg_color}" +"{", file=text_file) 
                                get_id(graph_obj)
                                dict.update({class_name:ct})
                                ct = ct + 1
                         
                        if 'rdfs:subClassOf' not in  i and 'rdfs:isDefinedBy' not in i:
                            print("class " + "\"" + class_name + "\"" + " as " + class_name + f" {bg_color}" +"{", file=text_file)   
                            get_id(graph_obj)
                            
                        if 'rdfs:subClassOf' in  i and 'rdfs:isDefinedBy' not in i:
                            print("class " + "\"" + class_name + "\"" + " as " + class_name + "{", file=text_file) 
                            get_id(graph_obj)
                            
                        if "rdf:" in i["rdfs:subClassOf"]["@id"]:
                            spclass_name = i["rdfs:subClassOf"]["@id"]
                            superclass_name = "".join(spclass_name)
                            super_class = i["rdfs:subClassOf"]["@id"]
                            print("class " + "\"" + i["rdfs:subClassOf"]["@id"] + "\" "+ "as " + superclass_name, file=text_file)
                            if "rdf:" not in super_class:
                                super_class = super_class.split(":")
                                file_path = find_file(super_class[1]+ '.jsonld',voc_dir)
                                with open(file_path[0], "r+") as super_file:
                                    super_obj = json.load(super_file)
                                    graph(super_obj,cl_dir)
                            print(f'"{spclass_name}"' + " --|> " + f'"{class_name}"' + " : SubClass", file=text_file)
                        elif "rdf:" not in i["rdfs:subClassOf"]["@id"]:
                            spclass_name = i["rdfs:subClassOf"]["@id"]
                            superclass_name = "".join(spclass_name)
                            super_class = i["rdfs:subClassOf"]["@id"]
                            super_class = super_class.split(":")
                            file_path = find_file(super_class[1]+ '.jsonld',voc_dir)
                            with open(file_path[0], "r+") as super_file:
                                super_obj = json.load(super_file)
                                graph(super_obj,cl_dir)
                            print(f'"{spclass_name}"' + " --|> " + f'"{class_name}"' + " : SubClass", file=text_file)
                                    
        else:
            print("@graph missing in " + filename)
    except:
          pass


def prop_cond1(domain_includes,class_name,bg_color,text_color):
    domain_name = domain_includes['@id']
    dn1 = domain_includes['@id'].replace('adex:', '')
    jsonld_prop = find_file(dn1+".jsonld", voc_dir)
    global ct
    if not jsonld_prop:
        if domain_includes['@id'] in dict.keys():
            num = dict[domain_includes['@id']]
            print("class " + f'"{domain_name}<sup>{num}</sup>"'+ f" {bg_color}" +" {"  + "\n"  + f"<color:{text_color}>" + class_name  + "\n" + " }", file=text_file)
        if domain_includes['@id'] not in dict.keys():
            print("class " + f'"{domain_name}<sup>{ct}</sup>"'+ f" {bg_color}" + " {"  + "\n"  + f"<color:{text_color}>" + class_name  + "\n" + " }", file=text_file)
            dict.update({domain_includes['@id']:ct})
            ct = ct+1
    if jsonld_prop:
        with open(jsonld_prop[0], "r+") as obj_file:
            obj1 = json.load(obj_file)
        if "rdfs:subClassOf" not in obj1['@graph'][0] and obj1['@graph'][0]['rdfs:label'] != "Thing":
            print("class " + f'"{domain_name}"' + f" {bg_color}" +" {"  + "\n"  + f"<color:{text_color}>" + class_name  + "\n" + " }", file=text_file)
        else:
            print("class " + f'"{domain_name}"'  +" {"  + "\n"  + f"<color:{text_color}>" + class_name  + "\n" + " }", file=text_file)


def prop(obj):
    """ Generate PlantUML text.
    This function generates a text file from the properties,
    which is used by plantuml to generate the UML Ontology diagram for ADEX.
    """
    global ct

    if "@graph" in obj.keys():
        graph_obj = copy.deepcopy(obj["@graph"])
        for i in obj["@graph"]:
            property_name = i['rdfs:label']
            if property_name not in dup_property:
                if i["adex:domainIncludes"]:
                    rng_incl = []
                    for range_includes in  i["adex:rangeIncludes"]:
                        if range_includes['@id']:
                            range_includes =  {'@id':range_includes['@id']}
                    for domain_includes in  i["adex:domainIncludes"]:
                        if domain_includes['@id']:
                            domain_includes =  {'@id':domain_includes['@id']}
                            if range_includes['@id'] in dict.keys():
                                class_name = i["@id"]
                                num = dict[range_includes['@id']]
                                dn = domain_includes['@id']
                                if i["@type"] == ['adex:TimeProperty']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#red>" + class_name  + f"<sup>{num}</sup>"+ "\n" + " }", file=text_file)
                                if i["@type"] == ['adex:TextProperty']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#blue>" + class_name  +f"<sup>{num}</sup>"+ "\n" + " }", file=text_file)
                                if i["@type"] == ['adex:QuantitativeProperty']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#brown>" + class_name +f"<sup>{num}</sup>" + "\n" + " }", file=text_file)
                                if i["@type"] == ['adex:StructuredProperty']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#black>" + class_name + f"<sup>{num}</sup>" + "\n" + " }", file=text_file)
                                if i["@type"] == ['adex:GeoProperty']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#grey>" + class_name + f"<sup>{num}</sup>" + "\n" + " }", file=text_file)
                                if i["@type"] == ['adex:Relationship']:
                                    print("class " + f'"{dn}"' + " {"  + "\n"  + "<color:#green>" + class_name +f"<sup>{num}</sup>"+ "\n" + " }", file=text_file)
                                rng_incl.append(domain_includes['@id'])

                            if domain_includes['@id'] not in rng_incl and domain_includes['@id'] in dict.keys() :
                                class_name = i["@id"]
                                if i["@type"] == ['adex:TimeProperty']:
                                    text_color = "#red"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:TextProperty']:
                                    text_color = "#blue"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:QuantitativeProperty']:
                                    text_color = "#brown"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:StructuredProperty']:
                                    text_color = "#black"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:GeoProperty']:
                                    text_color = "#grey"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:Relationship']:
                                    text_color = "#green"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)

                            if domain_includes['@id'] not in rng_incl and domain_includes['@id'] not in dict.keys():
                                class_name = i["@id"]
                                if i["@type"] == ['adex:TimeProperty']:
                                    text_color = "#red"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:TextProperty']:
                                    text_color = "#blue"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:QuantitativeProperty']:
                                    text_color = "#brown"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:StructuredProperty']:
                                    text_color = "#black"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:GeoProperty']:
                                    text_color = "#grey"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                if i["@type"] == ['adex:Relationship']:
                                    text_color = "#green"
                                    prop_cond1(domain_includes,class_name,bg_color,text_color)
                                
                    dup_property.append(property_name)                          
    else:
        print("@graph missing in " + filename)
    

with open(os.path.join(diagram_path, 'adex-Vocab-Ontology.txt'), "w+") as text_file:
    print("@startuml", file=text_file)
    print("title ADEX-VOC Ontology Diagram", file=text_file)
    print("skinparam titleFontSize 30", file=text_file)
    print("skinparam titleFontColor DarkGoldenRod" + "\n", file=text_file)
    print("left to right direction" + "\n" + "skinparam classFontColor DarkCyan" + "\n" + "skinparam roundcorner 27" + "\n", file=text_file)
    print("skinparam legendBackgroundColor #FFFFFF"+ "\n", file=text_file)
    #Accessing all the Classes in agrijson
    dirs = glob.glob(os.path.join(voc_dir, '*'))
    class_dirs = find_name('classes',voc_dir)
    try:    
        for cl_dir in class_dirs:
            sub_dirs = glob.glob(os.path.join(cl_dir, '*.jsonld'))
            for cl_filename in sub_dirs:
                with open(cl_filename, "r+") as obj_file:
                    obj = json.load(obj_file)
                    graph(obj,cl_dir)
    except:
        print("Error in Json file") 
    #Accessing all the Properties in agrijson
    try:
        property_dirs = find_name('properties',voc_dir)
        for dir in property_dirs:
            sub_dirs = glob.glob(os.path.join(dir, '*.jsonld'))
            for filename in sub_dirs:
                with open(filename, "r+") as obj_file:
                    obj = json.load(obj_file)
                    prop(obj)
    except:
        print("Json file is empty")  

    print(""" 
    legend
    <back:red>     </back> TimeProperty         <back:blue>     </back> TextProperty         <back:brown>     </back> QuantitativeProperty         <back:black>     </back> StructuredProperty         <back:grey>     </back> GeoProperty         <back:green>     </back> Relationship 
    endlegend""", file=text_file)            
    print("\n" + "@enduml", file=text_file)
    


#Install Java "sudo apt install default-jre"
plantuml_path = os.path.join(voc_dir,'utils/misc/plantuml.jar')
out_path = os.path.join(diagram_path, 'adex-Vocab-Ontology.txt')
subprocess.check_output(f'java -jar -DPLANTUML_LIMIT_SIZE=20000 {plantuml_path} {out_path}', shell=True, text=True)


#Install packages for png to pdf "sudo apt-get install python3-pil tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-script-latn"
png_path = os.path.join(diagram_path,"adex-Vocab-Ontology.png")
pdf_path = os.path.join(diagram_path,"adex-Vocab-Ontology.pdf")
PDF = pytesseract.image_to_pdf_or_hocr(png_path, extension='pdf')
# export to searchable.pdf
with open(pdf_path, "w+b") as f:
    f.write(bytearray(PDF))

