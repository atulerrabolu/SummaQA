from modules.questions import Questions
from modules.modelqa import ModelQA
from modules.webscraper import WebScraper
from summa.summarizer import summarize

class Summarizer:
	def __init__(self, topic, numLinks, questionsList, api_key, model, tokenizer):
		self.topic = topic
		self.numLinks = numLinks
		self.questionsList = questionsList
		self.api_key = api_key
		self.model = model
		self.tokenizer = tokenizer

	def getSummary(self):
		#gets all the text from the sites
		text = WebScraper(topic=self.topic, numLinks=self.numLinks, api_key=self.api_key).getAllText()
		
		#gets the components that make up the summary
		qAndA = self.getQuestionsAndAnwers(text=text)
		overview = self.getOverview(text=text, words=100)

		summary = qAndA + '\n\nSummary:\n' + overview #merge the question and answers to the overall summary

		return summary.strip()

	#gets the string for the questions and answers output
	def getQuestionsAndAnwers(self, text):
		answers = self.getAnswers(text=text)
		#create string that has the question above each answer
		qAndA = ''
		for i in range(len(self.questionsList)):
			answer = answers[i] if answers[i] != 'N/A' else ''
			qAndA += self.questionsList[i] + '\n' + answer

		return qAndA

	#gets the string of an overall summary on the topic that limited to some number of words
	def getOverview(self, text, words):
		overview = summarize(text, words=words)
		return overview

	#returns a list of the answers
	def getAnswers(self, text):
		model = ModelQA(questionList=self.questionsList,
						source=text,
						model=self.model,
						tokenizer=self.tokenizer)
		answers = model.getAnswers()
		return answers