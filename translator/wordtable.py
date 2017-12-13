import numpy as np


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
