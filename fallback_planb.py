import requests
import json
positive = [
    "I have fever",
    "I have cold",
    "I'm suffering from fever",
    "I had paracetamol",
    "I have diarrhea",
    "i have a car",
    "i have coffee",
    "i've been going out",
    "i want mexican food",
    "i bought a car",
    "how are you",
    "let's go",
    "I will come",
    "I have done that",
    "I wil watch TV",
    "I have homework",
    "I have homework to do",
    "I have a cycle",
    "I have a tumor"

]


concepts = []
all_rows = []
all_entities = []
def getCUI(entity):
    global concepts
    res = requests.get("http://localhost:8000/concepts", {"terms": ",".join(entity), "partial" : "1"})
    res_json = res.json()
    concepts = res_json


def serialize(response):
    entities = response["entities"]
    intentRanking = response["intent_ranking"]
    text = response["text"]
    intent = response["intent"]
    if intent == None:
        return ''
    row = [text, intent["name"]+":"+str(intent["confidence"])]
    i = 0
    for ent in entities[0:2]:

        all_entities.append(ent["value"])
        row.append(ent["entity"]+":"+ent["value"])
        i += 1
    row.extend([" "]*(2-i))
    for intentRank in intentRanking:
        row.append(intentRank["name"] + ":"+str(intentRank["confidence"]))
        #row.append(str(intentRank["confidence"]))
    return ",".join(row)
def makeCall(statementsArray, port):
    global all_rows
    for statement in statementsArray:
        res = requests.get("http://localhost:" + str(port) +"/parse", {"q": statement})
        res_json = res.json()
        all_rows.append(serialize(res_json))
    all_rows.append("\n")
makeCall(positive, 5001)

getCUI(entity=all_entities)
print(json.dumps(concepts))
print(all_entities)