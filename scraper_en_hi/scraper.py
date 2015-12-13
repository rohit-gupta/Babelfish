# -*- coding: utf-8 -*- 
# Python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import re
import sys

loc            = 'comparable_hi_en_corpus/'
no_eng_found   = 0
page_count     = 0
all_done       = ''
hindi_alphabet = 'कखगघतथदधपफबभचछजझटठडढनमवलयशर'
search_url     = 'https://hi.wikipedia.org/w/api.php?format=xml&action=query&list=allpages&apprefix='
url_flags      = '&aplimit=max'
page_base_url  = 'https://hi.wikipedia.org/?curid='
header         = {'User-Agent': 'BabelfishScraper/0.1'}

for letter in hindi_alphabet:
	f_url=search_url+quote(letter)+url_flags
	page1=urlopen(f_url).read()
	soup1=BeautifulSoup(page1)
	for tag in soup1.find_all('p'):
		print(no_eng_found)
		print(page_count)
		hi_url = page_base_url+tag['pageid']
		hi_page = urlopen(hi_url).read().decode('utf-8')
		hi_page = re.sub('<td.*?</td>', '', hi_page,flags=re.DOTALL)
		hi_page = re.sub('<tr.*?</tr>', '', hi_page,flags=re.DOTALL)
		hi_page = re.sub('<table.*?</table>', '', hi_page,flags=re.DOTALL)
		soup = BeautifulSoup(hi_page)
		link = soup.find("a", { "lang" : "en" })
		if link is None:
			no_eng_found=no_eng_found+1
			continue
		else:
			page_count=page_count+1
			en_url='https:'+link['href']

		hi_str=''
		en_str=''
		for tag in soup.find_all('p'):
			hi_str=hi_str+tag.text+'\n'
	
		en_page = urlopen(en_url).read().decode('utf-8')
		en_page = re.sub('<td.*?</td>', '', hi_page,flags=re.DOTALL)
		en_page = re.sub('<tr.*?</tr>', '', hi_page,flags=re.DOTALL)
		en_page = re.sub('<table.*?</table>', '', hi_page,flags=re.DOTALL)
		soup = BeautifulSoup(hi_page)
		for tag in soup.find_all('table'):
			del tag
		for tag in soup.find_all('p'):
			en_str=en_str+tag.text+'\n'
	
		hi_str=re.sub('\(.*?\)', '', hi_str,flags=re.DOTALL)
		hi_str=re.sub('\[.*?\]', '', hi_str,flags=re.DOTALL)
		en_str=re.sub('\(.*?\)', '', en_str,flags=re.DOTALL)
		en_str=re.sub('\[.*?\]', '', en_str,flags=re.DOTALL)
		hi=open(loc+str(page_count)+'_hi.txt','w')
		en=open(loc+str(page_count)+'_en.txt','w')
		hi.write(hi_str)
		en.write(en_str)
		hi.close()
		en.close()

