import spacy
from spacy.vocab import Vocab

clinical_nlp = spacy.load('en')
nlp = spacy.load('en')
txt = open("./try_model_vec.txt", 'r')
#clinical_nlp.vocab.load_vectors(txt)

# newVocab = Vocab()
# newVocab.load_vectors(txt)
clinical_nlp.vocab.load_vectors(txt)
#clinical_nlp.vocab.resize_vectors(300)

clinical_nlp.save_to_directory("./new_vocab/clinical")
clinical_nlp.vocab.dump_vectors('./new_vocab/clinical/vocab/vec.bin')

doc = clinical_nlp(u'I have fever')
doc2 = nlp(u'I have fever')
doc3 = clinical_nlp(u'I have coffee')
doc4 = nlp(u'I have coffee')


tokens = [doc.__getitem__(1), doc2.__getitem__(1), doc.__getitem__(2), doc2.__getitem__(2), doc3.__getitem__(2), doc4.__getitem__(2)]
print(tokens)
print("cli:have, cli:fever", tokens[0].similarity(tokens[2]))
print("en:have, en:fever", tokens[1].similarity(tokens[3]))
print("cli:have, cli:coffee", tokens[0].similarity(tokens[4]))
print("en:have, en:coffee", tokens[1].similarity(tokens[5]))
print("cli:fever, cli:coffee", tokens[2].similarity(tokens[4]))
print("en:fever, en:coffee", tokens[3].similarity(tokens[5]))
# print(doc)
# for word in doc:
#     print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
#
# for word in doc:
#     print(word.text, word.ent_iob, word.ent_type_)