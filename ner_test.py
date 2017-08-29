import requests
import json
f = open("testdata.json", "r")

#positive = json.load(f)
positive = [
    "I have fever",
    "I have cold",
    "I'm suffering from fever",
    "I had paracetamol",
    "I have diarrhea"

]


negative = [
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
        row.append(ent["entity"]+":"+ent["value"])
        i += 1
    row.extend([" "]*(2-i))
    for intentRank in intentRanking:
        row.append(intentRank["name"] + ":"+str(intentRank["confidence"]))
        #row.append(str(intentRank["confidence"]))

    return ",".join(row)
all_rows = []

def makeCall(statementsArray, port):
    global all_rows
    for statement in statementsArray:
        res = requests.get("http://localhost:" + str(port) +"/parse", {"q": statement})
        res_json = res.json()
        all_rows.append(serialize(res_json))
    all_rows.append("\n")
def clinical():
    global all_rows
    all_rows = ["Text,Intent,entitie1,entitie2"]
    makeCall(positive, 5000)
    makeCall(negative, 5000)
    f = open("clinical_vocab.csv","w")
    for row in all_rows:
        f.write(row+"\n")
def normal():
    global all_rows
    all_rows = ["Text,Intent,entitie1,entitie2"]
    makeCall(positive, 5001)
    makeCall(negative, 5001)
    f = open("normal_vocab.csv","w")
    for row in all_rows:
        f.write(row+"\n")
clinical()
print(all_rows)
normal()
print(all_rows)
print("done")