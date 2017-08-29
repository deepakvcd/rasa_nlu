import json

f = open("umls2.json", "r")
json_dis = json.load(f)
diseases = []
for obj in json_dis:
    if u' ' not in obj["STR"]:
        diseases.append(obj["STR"])
print diseases