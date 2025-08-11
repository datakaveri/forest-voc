import json
import os
import copy

dm = input("Enter the name of the data model -")
print("datamodel :", dm)
datamodels = os.listdir("../../data-models")
file = {}
file["@context"] = "https://agrijson.org/"
file["type"] = [
    "adex:" + dm,
    "adex:Schema"
]
file["id"] = "https://agrijson.org/" + dm

SPs = []
SP1s = []
schema = {}


schema["title"] = "ADEX " + dm + " Data Model"
schema["type"] = "object"
schema["properties"] = {}
schema["properties"]["type"] = {
    "type": "array",
    "items": [{
        "type": "string",
        "description": "ADEX Data Model name. It has to be " + dm
    },
        {
            "type": "string",
            "description": "ADEX Entity type. It has to be Resource"
        }
    ]
}
typeMapping = {
    "adex:QuantitativeProperty": "number",
    "adex:TextProperty": "string",
    "adex:TimeProperty": "string",
    "adex:StructuredProperty": "object",
    "adex:Relationship": "object",
    "adex:GeoProperty": "object"
}
relationshipValueProperties = {
    "isRelatedTo": {
        "type": "string",
        "description": "Value associated with RelationshipValue class. Contains IRI(s) that specify the relationship object(s)."
    },
    "hasObject": {
        "type": "string",
        "description": "Value associated with RelationshipValue class. Contains IRI(s) that specify the relationship object(s)."
    },
    "name": {
        "type": "string",
        "description": "Name of the entity."
    },
    "relationType": {
        "type": "string",
        "description": "Type of relation. ENUM: [REL_MESSAGESTREAM, REL_FILE, REL_DATASET, REL_THING]."
    }
}
baseSchemaPropPath = "../../base-schemas/properties/"
commonPropertiesPath = "../../data-models/Common/properties/"

def SchemaProperties(prop, dict, splist):
    propName = prop["@graph"][0]["@id"].split("adex:")[1]
    dataType = prop["@graph"][0]["@type"][0]
    propType = typeMapping[dataType]
    propDesc = prop["@graph"][0]["rdfs:comment"]
    dict["properties"][propName] = {}
    dict["properties"][propName]["type"] = propType
    dict["properties"][propName]["description"] = propDesc
    if dataType == "adex:TextProperty":
        if "'@container': '@list'" in str(prop["@graph"][0]["adex:rangeIncludes"]):
            dict["properties"][propName]["type"] = "array"
            dict["properties"][propName]["items"] = {"type": "string"}
    if dataType == "adex:QuantitativeProperty":
        dict["properties"][propName]["unitCode"] = ""
        dict["properties"][propName]["unitText"] = ""
        if "'@id': 'adex:NumericArray'" in str(prop["@graph"][0]["adex:rangeIncludes"]):
            dict["properties"][propName]["type"] = "array"
            dict["properties"][propName]["items"] = {"type": "number"}
    if dataType == "adex:TimeProperty":
        dt = {"@id": "adex:DateTime"}
        if dt in prop["@graph"][0]["adex:rangeIncludes"]:
            dict["properties"][propName]["format"] = "date-time"
        else:
            dict["properties"][propName]["format"] = "time" if "time" in propName.lower() else "date"
    if dataType == "adex:StructuredProperty":
        # print("propName ", propName)
        spClassName = prop["@graph"][0]["adex:rangeIncludes"][0]["@id"].split("adex:")[1]
        splist.append(propName + "|" + spClassName)
    if dataType == "adex:Relationship":
        dict["properties"][propName]["properties"] = relationshipValueProperties
    return dict

def Schema(path, domainName, isSP):
    obj = {}
    for prop in os.listdir(path):
        f = open(path + prop)
        prop = json.load(f)
        for domain in prop["@graph"][0]["adex:domainIncludes"]:
            if domain["@id"] == "adex:" + domainName:
                if isSP == "Yes":
                     obj = SchemaProperties(prop, schematmp, SP1s)
                else:
                    obj = SchemaProperties(prop, schema, SPs)

    return obj

Schema(baseSchemaPropPath, dm, None)

for dir in datamodels:
    dmDirPath = "../../data-models/" + dir
    if "properties" in os.listdir(dmDirPath):
        dmPropPath = "../../data-models/" + dir + "/properties/"
        Schema(dmPropPath, dm, None)

# print("SPs", SPs)
for item in SPs:
    propName = item.split("|")[0]
    name = item.split("|")[1]
    if name in datamodels:
        path = "../../data-models/" + name + "/properties/"
        # print("SP PATH --- ", path)
    elif name + ".jsonld" in "../../base-schemas/classes":
        path = baseSchemaPropPath
    else:
        path = "DM_path"
    schematmp = {}
    schematmp["properties"] = {}
    if os.path.exists(path):
        spSchema = Schema(path, name, "Yes")
        schema["properties"][propName]["properties"] = spSchema["properties"] if spSchema != {} else {}
    else:
        print("Add SP schema manually - ", item)
SchemaFile = file
file["schema"] = schema
# print("Schema ----- ", json.dumps(schema))
# print("File ----- ", json.dumps(file))

json_object = json.dumps(file, indent=4)
with open("../../examples/ex_"+dm+"_schema.jsonld", "w") as outfile:
    outfile.write(json_object)