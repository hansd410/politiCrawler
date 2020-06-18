import os
import re
from tqdm import tqdm

from bs4 import BeautifulSoup

def listToStr(inputList):
	outputString = ""
	for entity in inputList:
		if (outputString !=""):
			outputString += ", "
		outputString += entity
	return outputString

fileDir = "crawled"
fileNameList = os.listdir(fileDir)

nullPageIdList = []
errorPageIdList = []
fout = open("parsed.txt",'w')
log = open("log.txt",'w')

for fileName in tqdm(fileNameList):
	#print("read "+fileName)
	fin = open(fileDir+"/"+fileName,'r')
	text = fin.read()
	label = -1

	# filter "Here's a fact: You ended up in the wrong place!"
	if("You ended up in the wrong place" in text):
		nullPageIdList.append(fileName)
		continue
	#print("processing "+fileName)
	# html parse 
	bs = BeautifulSoup(text, 'html.parser')

	# get statement
	try:
		statementSection = bs.find('section', attrs={'class':'o-stage'})
	except:
		errorPageIdList.append(fileName)
		continue
	try:
		statement = statementSection.find('div',attrs={'class':'m-statement__quote'}).contents[0].rstrip().lstrip().replace("\n"," ")
	except:
		errorPageIdList.append(fileName)
		continue

	# get label
	try:
		pictures = statementSection.find_all('picture')
	except:
		errorPageIdList.append(fileName)
		continue
	for picture in pictures:
		if(picture.find('img').has_attr('alt')):
			label = picture.find('img')['alt']
	if(label ==-1):
		errorPageIdList.append(fileName)
		continue

	# get news info
	try:
		newsSection = bs.find('section', attrs={'id':'sources'})
	except:
		errorPageIdList.append(fileName)	
		continue

	newsPs = newsSection.findAll('p')
	newsList = []
	for newsP in newsPs:
		try:
			newsLink = newsP.find('a')['href']
		except:
			newsLink = "null"
		try:
			newsTitle = str(newsP.find('a').contents[0]).replace("<u>","").replace("</u>","").rstrip().lstrip()
		except:
			newsTitle = "noTitle"
		newsList.append([str(newsLink),str(newsTitle)])
	newsListString = "<"
	for newsPair in newsList:
		[newsLink,newsTitle] = newsPair
		if newsListString != "<":
			newsListString += "||"
		if(newsTitle != "noTitle" or newsLink != "null"):
			newsListString += newsTitle+"|"+newsLink
	newsListString += ">"
	
	fout.write(fileName+"\t"+statement+"\t"+label+"\t"+newsListString+"\n")

log.write("null pages\n")
log.write(listToStr(nullPageIdList)+"\n")
log.write("error pages\n")
log.write(listToStr(errorPageIdList))


