# coding: utf-8

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from gensim import corpora, models, similarities


data_dir ='triplets/'
article_id = 2
THRESHOLD = 0.75

native_file     = open(data_dir+str(article_id)+'_en.txt','r')
hindi_file      = open(data_dir+str(article_id)+'_hi.txt','r')
translated_file = open(data_dir+str(article_id)+'_tr_en.txt','r')
native          = native_file.read().splitlines()
hindi           = hindi_file.read().splitlines()
translated      = translated_file.read().splitlines()

# remove common words and tokenize
stoplist = set('of for a an the and to in it is'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in native]
# remove words that appear only once
# from collections import defaultdict
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1
# texts = [[token for token in text if frequency[token] > 1]
#          for text in texts]
# from pprint import pprint   # pretty-printer
# pprint(texts)



dictionary = corpora.Dictionary(texts)


corpus = [dictionary.doc2bow(text) for text in texts]

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=5)

for itr,query in enumerate(translated):

	vec_bow = dictionary.doc2bow(query.lower().split())
	vec_lsi = lsi[vec_bow] # convert the translated to LSI space
	#print(vec_lsi)


	index = similarities.MatrixSimilarity(lsi[corpus])


	sims = index[vec_lsi]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	if sims[0][1] >= 0:
		print(sims[0][1])
		print(hindi[itr])
		print(translated[itr])
		print(native[sims[0][0]])