import sys 
import xml.etree.ElementTree as ET
import re


string1='files/'
string3='files1/'
count1=1
file2=open('d.txt','w')
while count1 <= 10000:
	text=open(string1+str(count1)+'.txt','r').readlines()
	alert=0
	ind1=0
	ind2=0
	count=0

	
	text2=''
	for lines in text:
		text2=text2+lines
	
	#file1=open('temp.xml','w')
	#file1.write(text2)	
	#file1.close
	#text2='<link a a a> asdf (h ./8*_)<link asd> a </link> </link>'		
	text2=re.sub('<link.*?>', '', text2,flags=re.DOTALL)	
	text2=re.sub('</link.*?>', '', text2,flags=re.DOTALL)
	text2=re.sub('<math.*?</math>', '', text2,flags=re.DOTALL)
	text2=re.sub('<table.*?</table>', '', text2,flags=re.DOTALL)
	text2=re.sub('<cell.*?</cell>', '', text2,flags=re.DOTALL)
	text2=re.sub('<h.*?</h>', '', text2,flags=re.DOTALL)
	text2=re.sub('\(.*?\)', '', text2,flags=re.DOTALL)

	#removing stray elements
	text2=re.sub('<.?link>', '', text2,flags=re.DOTALL)
	text2=re.sub('<.?math>', '', text2,flags=re.DOTALL)
	text2=re.sub('<.?table>', '', text2,flags=re.DOTALL)
	text2=re.sub('<.?cell>', '', text2,flags=re.DOTALL)	
	text2=re.sub('<.?h>', '', text2,flags=re.DOTALL)

	try:
		root = ET.fromstring(text2)
	#root = tree.getroot()
	except:
		file2.write(str(count1)+'\n')	
		count1=count1+1
		print(count1)
		continue
	
	count=0

	for part in root.findall('article'):
		count=count+1
		if count==2:
			file1.close()
		if part.attrib['lang'] == 'en':
			file1=open(string3+str(count1)+'en.txt','w')
		else:
			file1=open(string3+str(count1)+'fr.txt','w')
		for part1 in part.findall('content'):
			for child in part1:
				if child.text is not None:
					file1.write(child.text)
	file1.close()
	count1=count1+1
	#print(count1)
	if count1%1000==0:
		print(count1/100)
	
	
	
