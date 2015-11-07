# -*- coding: utf-8 -*- 
# Python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import re
import sys

loc='comparable_hi_eng2/'
not_f=0
p_count=0
all_done=''
str1='कखगघतथदधपफबभचछजझटठडढनमवलयशर'
url1='https://hi.wikipedia.org/w/api.php?format=xml&action=query&list=allpages&apprefix='
url2='&aplimit=max'
url_1='https://hi.wikipedia.org/?curid='
header = {'User-Agent': 'Mozilla/5.0'}
txt1=''
for letter in str1:
	f_url=url1+quote(letter)+url2
	page1=urlopen(f_url).read()
	soup1=BeautifulSoup(page1)
	for tag in soup1.find_all('p'):
		print(not_f)
		print(p_count)
		url=url_1+tag['pageid']
		mainPage = urlopen(url).read().decode('utf-8')
		mainPage=re.sub('<td.*?</td>', '', mainPage,flags=re.DOTALL)
		mainPage=re.sub('<tr.*?</tr>', '', mainPage,flags=re.DOTALL)
		mainPage=re.sub('<table.*?</table>', '', mainPage,flags=re.DOTALL)
		soup = BeautifulSoup(mainPage)
		link = soup.find("a", { "lang" : "en" })
		if link is None:
			not_f=not_f+1
			continue
		else:
			p_count=p_count+1
			en_link='https:'+link['href']

		hi_str=''
		en_str=''
		for tag in soup.find_all('p'):
			hi_str=hi_str+tag.text+'\n'
	
		mainPage = urlopen(en_link).read().decode('utf-8')
		mainPage=re.sub('<td.*?</td>', '', mainPage,flags=re.DOTALL)
		mainPage=re.sub('<tr.*?</tr>', '', mainPage,flags=re.DOTALL)
		mainPage=re.sub('<table.*?</table>', '', mainPage,flags=re.DOTALL)
		soup = BeautifulSoup(mainPage)
		for tag in soup.find_all('table'):
			del tag
		for tag in soup.find_all('p'):
			en_str=en_str+tag.text+'\n'
	
		hi_str=re.sub('\(.*?\)', '', hi_str,flags=re.DOTALL)
		hi_str=re.sub('\[.*?\]', '', hi_str,flags=re.DOTALL)
		en_str=re.sub('\(.*?\)', '', en_str,flags=re.DOTALL)
		en_str=re.sub('\[.*?\]', '', en_str,flags=re.DOTALL)
		hi=open(loc+str(p_count)+'_hi.txt','w')
		en=open(loc+str(p_count)+'_en.txt','w')
		hi.write(hi_str)
		en.write(en_str)
		hi.close()
		en.close()
		

