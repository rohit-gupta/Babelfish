# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import model_from_json
import numpy as np
from six.moves import range
import json


TRAINING_SIZE = 50000
INVERT = True

HIDDEN_SIZE = 512
BATCH_SIZE = 128
LAYERS = 1
MAXLEN = 15
VOCAB=5000


class WordTable(object):
    """
    Given a sentence:
    + Encode it to a one hot integer representation
    + Decode the one hot integer representation to its character output
    + Decode a vector of probabilties to their character output
    """
    def __init__(self, words, maxlen):
        self.words = sorted(set(words))
        self.word_index = dict((w, i) for i, w in enumerate(self.words))
        self.index_word = dict((i, w) for i, w in enumerate(self.words))
        self.maxlen = maxlen

    def encode(self, sentence, maxlen=None):
        maxlen = maxlen if maxlen else self.maxlen
        X = np.zeros((maxlen, len(self.words)+1))
        for i, w in enumerate(sentence):
            X[i, self.word_index.get(w,len(self.words))] = 1
        return X

    def decode(self, X, calc_argmax=True):
        if calc_argmax:
            X = X.argmax(axis=-1)
        return ' '.join([self.index_word.get(x,"<UNK>") for x in X])

with open("HiEncode.txt") as f:
    hindi_words = f.read().strip().split("\n")

with open("EngEncode.txt") as f:
    english_words = f.read().strip().split("\n")

hindi_table   = WordTable(hindi_words,MAXLEN)
english_table = WordTable(english_words,MAXLEN)



with open('Translation_Model.mdl') as data_file:    
    model_json = json.load(data_file)

model = model_from_json(model_json)

model.load_weights('Translation_Model_Weights.h5')

indices1 = np.arange(1)
test1=np.zeros((1, MAXLEN, VOCAB), dtype=np.bool)
test1[0]=hindi_table.encode("जैसे ही भय आपके करीब आए उस पर आक्रमण कर उसे नष्ट कर दीजिये".split(' '))
test11=test1[indices1]
y_pred = (model.predict([test11]))
print(y_pred[0])
y_pred1=english_table.decode(y_pred[0])
print(y_pred1)