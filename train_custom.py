import json
import random
symptom_templates = [
    "I am having",
    "I have a",
    "I have had",
    "I do have",
    "I was also having",
    "I was having",
    "I think I have",
    "I feel I have",
    "Could you check if I have",
    "I am suffering from",
    "Had the"
]

# f = open("umls2.json", "r")
# json_diseases = json.load(f)
# diseases = ["fever", "malaria", "cold", "headache", "typhoid"]
# for obj in json_diseases:
#     if u' ' not in obj["STR"]:
#         diseases.append(str(obj["STR"]).lower())
    #diseases.append(obj["STR"].encode('ascii', 'ignore').lower())

diseases = []
f = open("symptoms_new.json", "r")
json_diseases = json.load(f)
for obj in json_diseases:
    if u' ' not in obj:
        diseases.append(str(obj).lower())
    #diseases.append(obj.encode('ascii', 'ignore').lower())
diseases = ["fever", "malaria", "cold", "headache", "typhoid"]
train_len = int(0.8 * len(diseases))
test_len = len(diseases) - train_len
# diseases = []
# for obj in json_diseases:
#     print(obj)
#     diseases.append(obj.lower())
#


assessment_templates = [
    "I did take",
    "I took some",
    "I had some",
    "I had"
]

f = open("medicine.json", "r")
json_medicine = json.load(f)
medicine = []
for obj in json_medicine:
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
    "I am having",
    "I have a",
    "I have had",
    "I do have",
    "I was also having",
    "I was having",
    "I think I have",
    "I feel I have",
    "Could you check if I have"
]
test_sentences = []
for i in range(0,len(used_indexes)):
    if used_indexes[i] == False:
        for temp in test_templates:
            test_sentences.append(temp.lower() + " " + diseases[i])
print(test_sentences)
newF = open("testdata.json","w")
newF.write(json.dumps(test_sentences))



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
    #getCommonexamples(assessment_templates, medicine, "medicine", "assessment")

    rasa_nlu["rasa_nlu_data"] = {
        "common_examples": common_examples
    }
    json_data = json.dumps(rasa_nlu)
    f = open("./data/examples/rasa/umls.json", 'w')
    f.write(json_data)
    print(json_data)

createNERData()