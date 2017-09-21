import requests
import json
f = open("testdata.json", "r")

positive = json.load(f)

symptom_params = {"sources": ["SNOMEDCT_US", "ICD10CM"],
                  "sems": ["fndg", "sosy", "phsf", "dsyn", "tmco", "blor", "bpoc", "bdsu", "qlco", "qnco", "anst",
                           "phsu", "clnd", "antb", "bhvr"
                      , "biof", "horm", "humn", "hcpp", "inbe", "inpo", "medd", "menp", "ortf", "virs", "vita"]}

assessment_params = {"sources": ["ICD10CM"], "sems": ["dsyn", "tmco", "virs", "vita"]}
plan_params = {"sources": ["SNOMEDCT_US", "RXNORM"], "sems": ["clnd", "phsu", "antb", "lbpr", "lbtr", "diap", "topp"]}

semTypes = {
    "symptom" : symptom_params,
    "assessment" : assessment_params
}

concepts = {}
all_rows = []
all_entities = {}
metamapResp = {}

def getCUI(all_entities):
    global concepts
    for key,value in all_entities.iteritems():
        res = requests.get("http://localhost:8000/concepts", {"terms": ",".join(set(value)), "sabs" : ",".join(semTypes[key]["sources"]), "sty": ",".join(semTypes[key]["sems_sty"])})
        res_json = res.json()
        concepts[key] = res_json
def getsourceId(all_entities):
    concepts = {}
    for key,value in all_entities.iteritems():
        if len(value) == 0:
            continue
        res = requests.get("http://localhost:8000/concepts_bulk", {"terms": ",".join(set(value))})
        res_json = res.json()
        concepts[key] = res_json
    print json.dumps(concepts)
def categorize(resp):
    category_resp = {}
    category_name = ''
    for obj in resp:
        if obj["intent"] == None:
            continue
        elif obj["intent"]["name"] not in category_resp:
            category_name = obj["intent"]["name"]
            category_resp[category_name] = []
        if obj["intent"]["confidence"] > 0.4:
            category_resp[category_name].append(obj["text"])
    return category_resp


def lambdApi(category_resp):
    global metamapResp
    #str = ". ".join(strArr)
    for key,value  in category_resp.iteritems():
        str_values = str(". ".join(value))
        temp_args = semTypes[key]
    # temp_args = [
    #     "-R SNOMEDCT_US,ICD10CM",
    #     "-J fndg,sosy,phsf,dsyn,tmco,blor,bpoc,bdsu,qlco,qnco,anst,phsu,clnd,antb,bhvr,biof,horm,humn,hcpp,inbe,inpo,medd,menp,ortf,virs,vita"
    # ]
        payload = {"input": str_values,
                   "args": ["-R " + ",".join(temp_args["sources"]), "-J " + ",".join(temp_args["sems"])]}
        res =requests.post("https://sgm5quwy9l.execute-api.us-east-1.amazonaws.com/umls/umls", json=payload)
        metamapResp[key] = res.json()
    serializemetamapResp(metamapResp)
    #print(json.dumps(res.json()))
def serialize(response):
    entities = response["entities"]
    intentRanking = response["intent_ranking"]
    text = response["text"]
    intent = response["intent"]
    if intent == None:
        return ''
    row = [text, intent["name"]+":"+str(intent["confidence"])]
    if intent["name"] not in all_entities:
        all_entities[intent["name"]] = []
    i = 0
    for ent in entities[0:2]:

        all_entities[intent["name"]].append(ent["value"])
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
        all_rows.append(res_json)
    #all_rows.append("\n")
    print(json.dumps(all_rows))
    print(categorize(all_rows))
    lambdApi(categorize(all_rows))

def serializeHavocResp(resp):
    for key,value in resp.iteritems():
        for obj in value:
            print(key, obj["cui"])

def serializemetamapResp(resp):
    all_cuis = {}
    for key,value in resp.iteritems():
        cuis = []
        for phrases in value:
            for phrase in phrases["phrases"]:

                for candidate in phrase["highestMapping"]["candidates"]:
                    cuis.append(candidate["candidateCUI"])
                    print(candidate["candidatePreferred"], candidate["candidateCUI"])
        all_cuis[key] = cuis
    getsourceId(all_cuis)
    return all_cuis
makeCall(positive, 5001)

# getCUI(entity=all_entities)
# print("havoc")
# #print(json.dumps(concepts))
# serializeHavocResp(concepts)
#
# lambdApi(positive)
# print("lambda")
# #print(all_entities)
# serializemetamapResp(metamapResp)