# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import model_from_json
import numpy as np
from six.moves import range
import json
from wordtable import WordTable


TRAINING_SIZE = 50000
INVERT = True

HIDDEN_SIZE = 512
BATCH_SIZE = 128
LAYERS = 1
MAXLEN = 15
VOCAB=5000

vocab_folder = "vocabulary/"


with open(vocab_folder + "hindi.txt") as f:
    hindi_words = f.read().strip().split("\n")

with open(vocab_folder + "english.txt") as f:
    english_words = f.read().strip().split("\n")

hindi_table   = WordTable(hindi_words,MAXLEN)
english_table = WordTable(english_words,MAXLEN)



with open('Translation_Model.mdl') as data_file:    
    model_json = json.load(data_file)

model = model_from_json(model_json)

model.load_weights('Translation_Model_Weights.h5')

indices1 = np.arange(1)
test1=np.zeros((1, MAXLEN, VOCAB), dtype=np.bool)
test1[0]=hindi_table.encode("इसी कारण से रेमी सॉम से इतना अलग है".split(' '))
test11=test1[indices1]
y_pred = (model.predict([test11]))
print(y_pred[0])
y_pred1=english_table.decode(y_pred[0])
print(y_pred1)
