# coding: utf-8

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from gensim import corpora, models, similarities

THRESHOLD = 0.75

str1='align_triplet/'
count=2

file1=open(str1+str(count)+'_en.txt','r')
file2=open(str1+str(count)+'_hi.txt','r')
file3=open(str1+str(count)+'_tr_en.txt','r')
native1=file1.read().splitlines()
translated1=file3.read().splitlines()
original1=file2.read().splitlines()

#print(native)
#print(original)
#print(translated)

#native = [ "Please rise then for this minutes silence", "You have requested a debate on this subject in the course of the next few days during this part session"]
#translated = ["You want a debate on this in the coming days during this session","I invite you to stand for this minute of silence"]
#original = ["Vous avez souhaité un débat à ce sujet dans les prochains jours au cours de cette période de session","Je vous invite à vous lever pour cette minute de silence"]

original1=['कंगनी या टांगुन  मोटे अन्नों में दूसरी सबसे अधिक बोई जाने वाली फसल है खासतौर पर पूर्वी एशिया में', ' चीन में तो इसे ईसा पूर्व ६००० वर्ष से उगाया जा रहा है इसे चीनी बाजरा भी कहते है', ' यह एकवर्षीय घास है जिसका पौधा ४  ७ फीट ऊँचा होता है बीज बहुत महीन लगभग २ मिलीमीटर के होते है इनका रंग किस्म किस्म में भिन्न होता है जिनपे पतला छिलका होता है जो आसानी से उतर जाता है', ' भारत में तमिलनाडु में इसे तिनी कहते है इसे दलिए में मिला कर खाया जाता है व चीन में इसे छोटा चावल कहते है', 'हिन्दी  कंगनी कांकुन टांगुनसंस्कृत  कंगनी प्रियंगु कंगुक सुकुमार अस्थिसंबन्धनअंग्रेजी  फॉक्सटेल मिलेट इटालियन मिलेटमराठी  कांग काऊन रालगुजराती  कांगबंगाली  काऊन काकनी कानिधान कांगनी दानाचीन में यह प्रमुख मोटा अन्न है गरीब उत्तरी क्षेत्रों में तो यही मुख्य भोजन है अमेरिका तथा यूरोप में इसे चारे भूसे या पक्क्षियो के भोजन रूप में उगाया जाता है', ' यह गर्म मौसम की फसल है चारे भूसे के रूप में यह ७५ दिन में और अन्न के रूप में ९० दिन में तैयार हो जाती है इसका उत्पादन चारे के रूप में करने पे २०००० किलो भूसे के रूप में करने पे ४००० किलो और अन्न के रूप में करने पे ८00 किलो फसल हो जाती है', 'कम से कम ईसा पूर्व ६००० वर्ष से चीन में उत्पादित हो रहा है यूरोप में यह कम से कम ईसा पुर्व २००० वर्ष से उत्पादित हो रहा है', 'मिलेट पर लेख']

native1=['Foxtail millet  is the secondmost widely planted species of millet and the most important in East Asia', ' It has the longest history of cultivation among the millets having been grown in China since sometime in the sixth millennium BC', ' Other names for the species include dwarf Setaria foxtail bristle grass giant setaria green foxtail Italian millet German millet Chinese millet and Hungarian millet', 'Foxtail millet is an annual grass with slim vertical leafy stems which can reach a height of 120200cm ', 'The seedhead is a dense hairy panicle 530cm  long', 'The small seeds around 2mm  in diameter are encased in a thin papery hull which is easily removed in threshing', ' Seed color varies greatly between varieties', 'Seeds of foxtail milletMochiAwa Japanese foxtail milletNames for foxtail millet in other languages spoken in the countries where it is cultivated includeIn South India it has been a staple diet among people for a long time from the sangam period', ' It is popularly quoted in the old Tamil texts and is commonly associated with Lord Muruga and his consort Valli', 'In China foxtail millet is the most common millet and one of the main food crops especially among the poor in the dry northern part of that country', ' In Europe and North America it is planted at a moderate scale for hay and silage and to a more limited extent for birdseed', 'It is a warm season crop typically planted in late spring', ' Harvest for hay or silage can be made in 6570 days  and for grain in 7590 days ', ' Its early maturity and efficient use of available water make it suitable for raising in dry areas', 'Diseases of foxtail millet include leaf and head blast disease caused by Magnaporthe grisea smut disease caused by Ustilago crameri and green ear caused by Sclerospora graminicola', ' The unharvested crop is also susceptible to attack by birds and rodents', 'The wild antecedent of foxtail millet has been securely identified as Setaria viridis which is interfertile with foxtail millet; wild or weedy forms of foxtail millet also exist', ' Zohary and Hopf note that the primary difference between the wild and cultivated forms is their seed dispersal biology', ' Wild and weedy forms shatter their seed while the cultivars retain them', ' The earliest evidence of the cultivation of this grain comes from the Peiligang culture of China which also cultivated the common millet but foxtail millet became the predominant grain only with the Yangshao culture', 'Foxtail millet arrived in Europe later; carbonized seeds first appear in the second millennium BC in central Europe', ' The earliest definite evidence for its cultivation in the Near East is at the Iron Age levels at Tille Hoyuk in Turkey with an uncorrected radiocarbon date of about 600 BC']

translated1=['Cornice or Tangun coarse grains is the second most cultivated crops particularly in East Asia', '6000 years BC in China it is grown it is also known as Chinese millet', 'This oneyear grass seed whose plant is 4 to 7 feet high about 2 millimeters are very fine in their color variety varies Jinpe variety is thin rind is easily off', 'In Tamil Nadu in India it is called Tini Dlia it got eaten in China and says it is small rice', 'Hindi Cornice Cornice Kankun Tangunsnskrit Priyngu Kanguk delicate Asthisnbndhnangreji Foxtail Millet Italian Miletmrathi Kong Ralgujrati Kangbangali Kaun Kaun Kakni Kanidhan Danachin staff tree is in poor northern areas of the major coarse grain that is the staple food in the US and in Europe as the bait straw or food Pkkshio is grown', 'The warm weather crop fodder straw as it within 75 days and grain as 9 0 days is ready production as bait to pay 20000 kg of straw as PE 4000 kg and grain as 800 kg of the crop is on', 'At least 6000 years BC in China is produced in Europe at least 2000 years BC produced is pre', 'Articles on millet']


translated=["Cornice or Tangun coarse grains is the second most cultivated crops particularly in East Asia","6000 years BC in China it is grown it is also known as Chinese millet"]
original=["कंगनी या टांगुन  मोटे अन्नों में दूसरी सबसे अधिक बोई जाने वाली फसल है खासतौर पर पूर्वी एशिया में","चीन में तो इसे ईसा पूर्व ६००० वर्ष से उगाया जा रहा है इसे चीनी बाजरा भी कहते है"]
native=["The small seeds around 2mm  in diameter are encased in a thin papery hull which is easily removed in threshing","Wild and weedy forms shatter their seed while the cultivars retain them"]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in native]
# remove words that appear only once
#from collections import defaultdict
#frequency = defaultdict(int)
#for text in texts:
#     for token in text:
#         frequency[token] += 1
#texts = [[token for token in text if frequency[token] > 1]
#          for text in texts]
from pprint import pprint   # pretty-printer
#pprint(texts)



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
	print(sims)
	if sims[0][1] > 0:
		print(sims[0][1])
		print(original[itr])
		print(translated[itr])
		print(native[sims[0][0]])


