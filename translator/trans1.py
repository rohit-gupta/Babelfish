from textblob import TextBlob
import textblob
import re
import string
import os.path
import time

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

str2='comparable_hi_eng2/'
str3='align_triplet2/'
count1=1

#introduce newline
#strip punctuation
#remove non-ascii

while count1 <2000:
	if os.path.isfile(str2+str(count1+1)+'_en.txt'):
		a=0
	else:
		time.sleep(5)
		continue
	file1=open(str2+str(count1)+'_en.txt','r')
	print('\nprocessing '+str(count1))
	
	#clean english	
	print('clean eng')
	str1=file1.readlines()
	text=''
	for lines in str1:
		lines=re.sub('\.', '\n', lines)
		lines=lines.strip()
		for lines1 in lines.split('\n'):
			lines1=lines1.strip()
			if len(lines1)>1:
				text=text+lines1+'\n'
	
	text=text.strip()
	text = re.sub('''[/"/'!–@#$.,://-]''', '', text)
	text=strip_non_ascii(text)
	file1=open(str3+str(count1)+'_en.txt','w')
	file1.write(text)
	file1.close()
	
	
	#clean hindi
	print('clean hindi')
	file1=open(str2+str(count1)+'_hi.txt','r')
	str1=file1.readlines()
	text=''
	for lines in str1:
		text=text+lines
	text=re.sub('।', '\n', text)
	text=text.strip()
	
	text = re.sub('''[/"/'!@#$.–,://-]''', '', text)
	len1=0
	text1=''
	for lines in text.split('\n'):
		lines=lines.strip()
		if len(lines)>1:
			len1=0
			for c in lines:
				if ord(c)<127 and c!=' 'and c!='\n' and c!=',':
					len1=len1+1
			if (len1/(len(lines)))<0.1:
				text1=text1+lines+'\n'
	text1=text1.strip()
	file1=open(str3+str(count1)+'_hi.txt','w')
	file1.write(text1)
	
	file1.close()
	
	file2=open(str3+str(count1)+'_tr_en.txt','w')
	print('translating')
	trans=''
	for lines in text1.split('\n'):
		if(len(lines)<4):
			print(lines)
		blob = TextBlob(lines)
		try:
			ans=blob.translate(to="en")
		except textblob.exceptions.NotTranslated:
			ans=lines
			errors=open('errors.txt','a')
			errors.write(str(count1)+'\n')	
			errors.close()		
		ans1= re.sub('''[/"/'!@#$.,–://-]''', '', str(ans))
		ans1=strip_non_ascii(ans1)
		trans=trans+ans1+'\n'
	trans=trans.strip()
	file2.write(trans)
	count1=count1+1
	file2.close()

