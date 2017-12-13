# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
import numpy as np
from six.moves import range
import json

from wordtable import WordTable


TRAINING_SIZE = 50000
#INVERT = True

HIDDEN_SIZE = 512
BATCH_SIZE  = 128
LAYERS = 1
MAXLEN = 15
VOCAB  =5000

vocab_folder = "vocabulary/"
corpus_folder = "parallel_corpus/"


questions = []
expected = []
seen = set()

print('Loading parallel corpora...')

with open(corpus_folder + "english.txt") as f:
    english_corpus = f.read().strip().lower().split("\n")

with open(corpus_folder + "hindi.txt") as f:
    hindi_corpus = f.read().strip().split("\n")


print('Vectorization...')

with open(vocab_folder + "hindi.txt") as f:
    hindi_words = f.read().strip().split("\n")

with open(vocab_folder + "english.txt") as f:
    english_words = f.read().strip().split("\n")

hindi_table   = WordTable(hindi_words,MAXLEN)
english_table = WordTable(english_words,MAXLEN)

#len_corpus=len(english_corpus)
len_corpus = 50000
eng_encoded=np.zeros((len_corpus, MAXLEN, VOCAB), dtype=np.bool)
hindi_encoded=np.zeros((len_corpus, MAXLEN, VOCAB), dtype=np.bool)
for count in range(len_corpus):
    eng_encoded[count] = english_table.encode(english_corpus[count].split(' '))
    hindi_encoded[count] = hindi_table.encode(hindi_corpus[count].split(' '))


# Shuffle (X, y) in unison as the later parts of X will almost all be larger digits
first_half_indices = np.arange(len_corpus/2)
second_half_indices = np.arange(len_corpus/2+1,len_corpus)
#np.random.shuffle(indices)
X = hindi_encoded[first_half_indices]
y = eng_encoded[first_half_indices]

# Explicitly set apart 10% for validation data that we never train over
split_at = len(X) - len(X) / 10
(X_train, X_val) = (slice_X(X, 0, split_at), slice_X(X, split_at))
(y_train, y_val) = (y[:split_at], y[split_at:])

print(X_train.shape)
print(y_train.shape)
print('Build model...')
model = Sequential()

model.add(recurrent.GRU(HIDDEN_SIZE, input_shape=(None, VOCAB),return_sequences=False)) # encoder

model.add(RepeatVector(MAXLEN))

for _ in range(LAYERS):
    model.add(recurrent.GRU(HIDDEN_SIZE, return_sequences=True)) # decoder

# For each of step of the output sequence, decide which character should be chosen
model.add(TimeDistributedDense(VOCAB))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X_train, y_train, batch_size=BATCH_SIZE, nb_epoch=40, validation_data=(X_val, y_val), show_accuracy=True)
model.save_weights("Translation_Model_Big_Weights_40Epochs_HalfData.h5")

X = hindi_encoded[second_half_indices]
y = eng_encoded[second_half_indices]

# Explicitly set apart 10% for validation data that we never train over
split_at = len(X) - len(X) / 10
(X_train, X_val) = (slice_X(X, 0, split_at), slice_X(X, split_at))
(y_train, y_val) = (y[:split_at], y[split_at:])

print(X_train.shape)
print(y_train.shape)

print('Further train model...')

model.fit(X_train, y_train, batch_size=BATCH_SIZE, nb_epoch=40, validation_data=(X_val, y_val), show_accuracy=True)
model.save_weights("Translation_Model_Big_Weights_40Epochs_FullData.h5")

model_json = model.to_json()
with open('Translation_Model_Big_Structure.mdl', 'w') as outfile:
    json.dump(model_json, outfile)
