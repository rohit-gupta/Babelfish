# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
import numpy as np
from six.moves import range
import sys


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


questions = []
expected = []
seen = set()

print('Loading parallel corpora...')

with open("PCEng1.txt") as f:
    english_corpus = f.read().strip().split("\n")

with open("PCHindi1.txt") as f:
    hindi_corpus = f.read().strip().split("\n")


print('Vectorization...')

with open("HiEncode.txt") as f:
    hindi_words = f.read().strip().split("\n")

with open("EngEncode.txt") as f:
    english_words = f.read().strip().split("\n")

hindi_table   = WordTable(hindi_words,MAXLEN)
english_table = WordTable(english_words,MAXLEN)

count=0
#len_corpus=len(english_corpus)
len_corpus = 50000
eng_encoded=np.zeros((len_corpus, MAXLEN, VOCAB), dtype=np.bool)
hindi_encoded=np.zeros((len_corpus, MAXLEN, VOCAB), dtype=np.bool)
for count in range(len_corpus):
    eng_encoded[count] = english_table.encode(english_corpus[count].split(' '))
    hindi_encoded[count] = hindi_table.encode(hindi_corpus[count].split(' '))


# Shuffle (X, y) in unison as the later parts of X will almost all be larger digits
indices = np.arange(len_corpus)
#np.random.shuffle(indices)
X = hindi_encoded[indices]
y = eng_encoded[indices]

# Explicitly set apart 10% for validation data that we never train over
split_at = len(X) - len(X) / 10
(X_train, X_val) = (slice_X(X, 0, split_at), slice_X(X, split_at))
(y_train, y_val) = (y[:split_at], y[split_at:])

print(X_train.shape)
print(y_train.shape)
print('Build model...')
model = Sequential()

model.add(recurrent.GRU(HIDDEN_SIZE, input_shape=(None, 5000),return_sequences=False)) # encoder

model.add(RepeatVector(MAXLEN))

for _ in range(LAYERS):
    model.add(recurrent.GRU(HIDDEN_SIZE, return_sequences=True)) # decoder

# For each of step of the output sequence, decide which character should be chosen
model.add(TimeDistributedDense(5000))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X_train, y_train, batch_size=BATCH_SIZE, nb_epoch=2, validation_data=(X_val, y_val), show_accuracy=True)

model.save_weights('keras_w_50000_2')
indices1 = np.arange(2)
test1=np.zeros((2, MAXLEN, VOCAB), dtype=np.bool)
test1[0]=hindi_table.encode("बीमारी के सबसे साधारण संकेत व रोग लक्षण क्या हैं".split(' '))
test1[0]=hindi_table.encode("अब वह लड़का उन्हें दिखाई देना बंद हो गया था".split(' '))
test11=test1[indices1]
y_pred = (model.predict([test11]))
print(y_pred[0])
y_pred1=english_table.decode(y_pred[0])
print(y_pred1)
y_pred1=english_table.decode(y_pred[1])
print(y_pred1)
