#!/usr/bin/env bash
###python -m spacy package ./new_vocab/clinical ./mymodels <<< $"\nclinical\n5.0\n\n\n\n\n\n\n"
set -x
VERSION="4.0"
model="mymodels/en_clinical_model-$VERSION"
port1=$(sudo lsof -n -i :8000 | grep LISTEN | cut -d' ' -f3)
port2=$(sudo lsof -n -i :5000 | grep LISTEN | cut -d' ' -f3)
echo $port1
echo $port2
sudo kill $port1
sudo kill $port2
if [ $1 == "train" ]; then
echo "
clinical_model
$VERSION






" | python -m spacy package ./new_vocab/clinical ./mymodels

cd $model
python setup.py sdist
cd dist
pip install "en_clinical_model-$VERSION.tar.gz"
sudo python -m spacy link en_clinical_model en_clinical_model
cd ../../..
python -m rasa_nlu.train -c config_spacy_clinical.json  --data="data/examples/rasa/umls.json"
python -m rasa_nlu.train -c config_spacy.json  --data="data/examples/rasa/umls.json"
elif [ $1 == "ner_train" ]; then
python -m rasa_nlu.train -c config_mitie.json --data="data/examples/rasa/umls.json"

fi

cd models
newNER=$(ls -td -- */ | head -n 1)
NER=$(ls -td -- */ | head -n 2 | tail -n 1)
cd ..
python -m rasa_nlu.server -c config_mitie.json --port=5001