import nltk
import pickle

word_freq_dict = {}
for word in nltk.corpus.brown.words():
    word = word.lower()
    word_freq_dict[word] = word_freq_dict.get(word, 0) + 1

pickle.dump(word_freq_dict, open("word_freq.pkl", "wb"))