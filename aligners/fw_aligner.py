# coding: utf-8

from fuzzywuzzy import fuzz

data_dir ='align_triplet1/'
article_id = 1
THRESHOLD = 60
LENGTH_FRAC_THRESHOLD = 0.50

while article_id<=30:

	native_file     = open(data_dir+str(article_id)+'_en.txt','r')
	hindi_file      = open(data_dir+str(article_id)+'_hi.txt','r')
	translated_file = open(data_dir+str(article_id)+'_tr_en.txt','r')
	native          = native_file.read().splitlines()
	hindi           = hindi_file.read().splitlines()
	translated      = translated_file.read().splitlines()

	# remove common words and tokenize
	stoplist = set('of for a an the and to in it is'.split())
	native_clean     = [' '.join([word for word in document.lower().split() if word not in stoplist]) for document in native]
	translated_clean = [' '.join([word for word in document.lower().split() if word not in stoplist]) for document in translated]
	
	for itr,query in enumerate(translated_clean):	
		max_match = 0
		for jtr, choice in enumerate(native_clean):
			if fuzz.token_set_ratio(query,choice) > max_match:
				max_match = fuzz.token_set_ratio(query,choice)
				best = jtr
	
		length_fraction = (len(translated[itr]) + 0.0)/len(native[best])
		if max_match >= THRESHOLD and length_fraction >= LENGTH_FRAC_THRESHOLD and length_fraction < 1/LENGTH_FRAC_THRESHOLD:
			filewr=open('parallel_corpus.txt','a')
			filewr.write("---\n")
			filewr.write(str(max_match)+'  '+str(round(length_fraction,3)))
			filewr.write('\n')
			filewr.write(hindi[itr])
			filewr.write('\n')
			#print translated[itr]
			filewr.write(native[best])
			filewr.write('\n')
			filewr.write(translated[itr])
			filewr.write('\n')	
	article_id=article_id+1
