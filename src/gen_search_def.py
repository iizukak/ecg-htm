import json
import pprint

JSON_PATH = "swarming/search_def_template.json"
JSON_OUT_PATH = "swarming/search_def_out.json"
FFT_LENGTH = 250

f = open(JSON_PATH, 'r')
w = open(JSON_OUT_PATH, 'w')
jsonData = json.load(f)

pprint.pprint(jsonData)
print(type(jsonData))

for i in range(FFT_LENGTH):
    field_name =  "f" + str(i)
    jsonData["includedFields"].append({
        "fieldName" : field_name,
        "fieldType" : "int"
    })
    jsonData["streamDef"]["aggregation"]["fields"].append(
        [field_name, "sum"]
    )

pprint.pprint(jsonData)

w.write(json.dumps(jsonData, sort_keys = True, indent = 4))
