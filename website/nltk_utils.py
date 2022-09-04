import nltk # imports the library nltk
from nltk.stem.porter import PorterStemmer# from the library nltk it will import the Stemmer of choice that I will be using
import numpy as np#imports the numpy library
stemmer=PorterStemmer()#creates an instance of PorterStemmer called stemmer
def tokenise(sentence):
    "module that takes in a sentence and tokenizes it"
    return nltk.word_tokenize(sentence)# 



def stem(word):
    "module that takes in a word and stems it"
    return stemmer.stem(word.lower())# returns the stemmed word note that the word becomes lower case 

def bag_of_words(tokenised_sentence,all_words):
    "module that will take in a tokenized sentence and will return a bag of words"
    tokenised_sentence=[stem(w) for w in tokenised_sentence]
    bag=np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenised_sentence:
            bag[idx]=1.0
    return bag




