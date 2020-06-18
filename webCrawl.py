import requests
from tqdm import tqdm
import json

saveDir = "crawled"

baseUrl = "https://www.politifact.com/factchecks/"
# crawls from latestId, # of crawlNum
latestId = 1
crawlNum = 1
for i in tqdm(range(latestId,latestId-crawlNum,-1)):
	url = baseUrl+str(i)+"/"	
	data = requests.get(url).text
	fout = open(saveDir+"/"+str(i),'w')
	fout.write(data)
