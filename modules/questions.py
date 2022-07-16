class Questions:
	def __init__(self, questionList):
		self.questionsList = questionList

	#get the correct question stem to help in the summary creation
	def getFormattedQuestions(self):
		'''
		1) chop off the uneccesary parts of the question sentence
		2) capitalize first letter in the remaining sentence and remove the question mark

		format key:
		What/Who: 3+ [IS] [ANS]
		Why: 3+ [BECAUSE] [ANS]
		When/Where: 3+ [IN] [ANS]
		How: 3+ [BY] [ANS]
		How ___ is: 4+ [IS] 

		3+/4+ means every word including and after the 3rd/4th word in the question
		'''

		formatted = []

		#create the correct form based on the question stem
		for qIdx in range(len(self.questionsList)):
			questionWords = self.questionsList[qIdx].split()
			firstWord = questionWords[0].lower()
			thirdWord = questionWords[2].lower()

			if firstWord == 'what' or firstWord == 'who':
				formatted.append(self.cleanString(' '.join(questionWords[2:])) + ' is ')
			elif firstWord == 'why':
				formatted.append(self.cleanString(' '.join(questionWords[2:])) + ' because ')
			elif firstWord == 'when':
				formatted.append(self.cleanString(' '.join(questionWords[2:])) + ' in ')
			elif firstWord == 'where':
				formatted.append(self.cleanString(' '.join(questionWords[2:])) + ' inside ')
			elif firstWord == 'how':
				if thirdWord == 'is':
					formatted.append(self.cleanString(' '.join(questionWords[3:])) + ' is ')
				else:
					formatted.append(self.cleanString(' '.join(questionWords[2:])) + ' through ')
			else:
				formatted.append(self.cleanString(' '.join(questionWords[2:])) + '- ')
		return formatted

	#clean up the sentence to help with formatting
	def cleanString(self, sentence):
		sentence = sentence[0].upper() + sentence[1:] #capitalize the first letter
		sentence = sentence[:-1] #remove the question mark
		return sentence