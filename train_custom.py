import json
import random
symptom_templates = [
    "I'm having",
    "I was suffering from",
    "I have a",
    "I've had",
    "I also had",
    "I do have",
    "Had the",
    "I was also having",
    "I was having",
    "I'm suffering from",
    "I think I have",
]

#diseases1 = ["fever", "chills", "common cold", "back pain"]
f = open("umls2.json", "r")
json_diseases = json.load(f)
diseases = []
for obj in json_diseases:
    # try:
    #     str(obj["STR"]).lower()
    #     diseases.append(str(obj["STR"]).lower())
    # except:
    #     pass
    if u' ' not in obj["STR"]:
        diseases.append(str(obj["STR"]).lower())
train_len = int(0.8 * len(diseases))
test_len = len(diseases) - train_len
# diseases = []
# for obj in json_diseases:
#     print(obj["STR"])
#     diseases.append(str(obj["STR"]).lower())



assessment_templates = [
    "I did take",
    "I took some",
    "I had some",
    "I had"
]

f = open("medicine.json", "r")
json_mdeicine = json.load(f)
medicine = []
for obj in json_mdeicine:
    # try:
    #     str(obj["STR"]).lower()
    #     diseases.append(str(obj["STR"]).lower())
    # except:
    #     pass
    #if u' ' not in obj["STR"]:
    medicine.append(str(obj["STR"]).lower())
medicine = ["Tylenol OTC", "paracetamol", "ajax", "dolo", "cold act"]
common_examples = []
trainRandomnumbersList = random.sample(xrange(0,len(diseases)), train_len)
#testRandomnumbersList = random.sample(xrange(0,len(diseases)), test_len)
used_indexes = [False] * len(diseases)

diseases_test = []
for i in trainRandomnumbersList:
    diseases_test.append(diseases[i])
    used_indexes[i] = True




test_templates = [
    "I have a",
    "I've got a",
    "I'm suffering from"
]
test_senetences = []
for i in range(0,len(used_indexes)):
    if used_indexes[i] == False:
        for temp in test_templates:
            test_senetences.append(temp.lower() + " " + diseases[i])
print(test_senetences)
newF = open("testdata.json","w")
newF.write(json.dumps(test_senetences))



def getCommonexamples(templates, values, entityValue, intent):
    global common_examples
    for temp in templates:

        for dis in values:
            common_example = {}
            entities = []
            common_example["text"] = temp.lower() + " " + dis
            common_example["intent"] = intent
            entity = {}
            entity["start"] = len(temp) + 1
            entity["end"] = entity["start"] + len(dis)
            entity["value"] = dis
            entity["entity"] = entityValue
            entities.append(entity)
            common_example["entities"] = entities
            common_examples.append(common_example)



def createWordVecData():
    gensem = []
    for template in symptom_templates:
        for disease in diseases:
            # print(disease)
            gensem.append(template.lower() + " " + disease.lower())
    print("\n".join(gensem))
    f = open("clinical.txt", 'w')
    f.write("\n".join(gensem))

def createNERData():
    rasa_nlu = {}
    global diseases1
    global medicine
    getCommonexamples(symptom_templates, diseases_test, "disease", "symptom")
    getCommonexamples(assessment_templates, medicine, "medicine", "assessment")

    rasa_nlu["rasa_nlu_data"] = {
        "common_examples": common_examples
    }
    json_data = json.dumps(rasa_nlu)
    f = open("./data/examples/rasa/umls.json", 'w')
    f.write(json_data)
    print(json_data)

createNERData()