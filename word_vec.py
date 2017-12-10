import json
import gensim
from collections import OrderedDict


from sklearn.manifold import TSNE
from sklearn.datasets import fetch_20newsgroups
import re
import matplotlib.pyplot as plt
import numpy as np
import codecs
from itertools import islice
#
# sentences = gensim.models.word2vec.LineSentence("./clinical.txt")
# temp_trans = gensim.models.Phrases(sentences, delimiter="_")
# bigram_transformer = gensim.models.Phrases(sentences, delimiter="_", threshold=1, min_count=1)
# model = gensim.models.Word2Vec(bigram_transformer[sentences], size=300, window=3, min_count=0, workers=4, hs=1)
# model.wv.save_word2vec_format('text.model.bin', binary=True)
# f = open("all_words.csv", "w")
# bigram_transformer.vocab = OrderedDict(sorted(bigram_transformer.vocab.items(), key=lambda t: t[1], reverse=True))
# for word in bigram_transformer.vocab:
#     f.write(word+","+str(bigram_transformer.vocab[word])+"\n")
# print(model.wv)
# model.wv.save_word2vec_format('word2vec_new_vocab.txt', binary=False)
# # f = open("word2vec_new_vocab.txt","w")
# # for word in model.wv.index2word:
# #     f.write(word+ " " + " ".join(str(x) for x in model.wv[word]) + "\n")
# similar = model.most_similar('fever')
# #print(model.wv.similarity('having', 'hypersplenism'))
# for sim in similar:
#     print(sim)


from gensim.models.keyedvectors import KeyedVectors


def main():
    embeddings_file = "PubMedw2v.txt"
    wv, vocabulary = load_embeddings(embeddings_file)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(wv[:1000, :])

    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()


def load_embeddings(file_name):
    with codecs.open(file_name, 'r', 'utf-8') as f_in:
        vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in
                               list(islice(f_in, 1000))])
    wv = np.loadtxt(wv)
    return wv, vocabulary


def createWordVecOf():
    sentences = gensim.models.word2vec.LineSentence("./clinical.txt")
    #temp_trans = gensim.models.Phrases(sentences, delimiter="_")
    bigram_transformer = gensim.models.Phrases(sentences, delimiter="_", threshold=1, min_count=4)
    model = gensim.models.Word2Vec(bigram_transformer[sentences], size=300, window=3, min_count=0, workers=4, hs=1)
    model.wv.save_word2vec_format('try.model.bin', binary=True)
    f = open("try_words.csv", "w")
    bigram_transformer.vocab = OrderedDict(sorted(bigram_transformer.vocab.items(), key=lambda t: t[1], reverse=True))
    for word in bigram_transformer.vocab:
        f.write(word+","+str(bigram_transformer.vocab[word])+"\n")
    print(model.wv)
    model.wv.save_word2vec_format('try_model_vec.txt', binary=False)


def drawGraph():
    embeddings_file = "try_model_vec.txt"
    wv, vocabulary = load_embeddings(embeddings_file)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(wv[:1000, :])

    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.show()

if __name__ == '__main__':
    #main()
    createWordVecOf()
    #drawGraph()
# model = KeyedVectors.load_word2vec_format('PubMedw2v.bin', binary=True)
# model.save_word2vec_format('PubMedw2v.txt', binary=False)

#model = KeyedVectors.load_word2vec_format('../PubMed-w2v.bin', binary=True)
# f = open("umls2.json", "r")
# json_diseases = json.load(f)
# for obj in json_diseases:
#     if u' ' in obj["STR"]:
#         continue
#     try:
#         print(obj, list(model.most_similar(str(obj['STR']))))
#     except:
#         print(str(obj['STR']), "no words")
# while True:
#     print("enter a word to find similarity")
#     txt1 =raw_input()
#     #txt2 = raw_input()
#     try:
#         print(list(model.most_similar(txt1)))
#         #print(list(model.most_similar(txt2)))
#         #print(model.wv.similarity(txt1, txt2))
#     except:
#         print("exception")

#
# X = model[model.wv.vocab]
#
# tsne = TSNE(n_components=2)
# X_tsne = tsne.fit_transform(X)
#
# plt.scatter(X_tsne[:, 0], X_tsne[:, 1])
# plt.show()
