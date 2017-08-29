import spacy

clinical_nlp = spacy.load('en_clinical_model')
nlp = spacy.load('en')

doc = clinical_nlp(u'fever and chills')
doc2 = nlp(u'fever and chills')

def printSimilarities(doc, doc2, firstVocab, secondVocab):
    for token1 in doc.__iter__():
        for token2 in doc2.__iter__():
            print(firstVocab+token1.text, secondVocab+token2.text, token1.similarity(token2))

printSimilarities(doc, doc2, "cli:", "en:")
printSimilarities(doc, doc, "cli:", "cli:")
printSimilarities(doc2, doc2, "en:", "en:")



print(doc.text)
# print(doc)
# for word in doc:
#     print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)
#
# for word in doc:
#     print(word.text, word.ent_iob, word.ent_type_)