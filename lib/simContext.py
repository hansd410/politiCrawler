from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def getSimContext(statement, contextList):
	corpus = [statement]+contextList
	vectorizer = TfidfVectorizer()
	Y = vectorizer.fit_transform(corpus)

	maxSimScore = 0
	maxSimIndex = 0
	simScoreList = cosine_similarity(Y[0],Y[1:])[0]
	for i in range(len(simScoreList)):
		score = simScoreList[i]
		if(maxSimScore<=score):
			maxSimIndex = i
			maxSimScore = score
	print(simScoreList)
	return contextList[maxSimIndex]


	
