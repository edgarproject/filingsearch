class Lectura(object):
	def __init__(self):
		self.configs = open('CONFIG.txt','r')
		self.configs = self.configs.readlines()


	def getKeydocs(self):
		return self.configs[0][8:].split()

	def getEnd(self):
		return self.configs[1][24:]

	def getKeyWords(self):
		keywords = []
		for i in range(5,5+int(self.configs[3][12:])):
			keywords.append(self.configs[i])
		return keywords

	def getFalseWord(self):
		false_word = []
		for i in range(12,12+int(self.configs[10][17:])):
			false_word.append(str(self.configs[i]))
		return false_word

	def getTypeSearch(self):
		option = int(self.configs[2][68:69])
		if option==1:
			urls = open('URLs.txt','r')
			urls = urls.readlines()
			allurls = []
			for url in urls:
				allurls.append(url)
			return allurls
		else:
			return "0"


