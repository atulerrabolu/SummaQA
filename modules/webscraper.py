import requests
from bs4 import BeautifulSoup
import re

class WebScraper:
	def __init__(self, topic, numLinks, api_key):
		self.topic = topic
		self.numLinks = numLinks #number of links
		self.api_key = api_key

	#get the combined text 
	def getAllText(self):
		links = self.getLinks()

		linkTexts = []
		for link in links:
			linkTexts.append(self.extractText(link)) #append each link's text into a list of texts

		return ' '.join(linkTexts) #combine all the link texts into one string
		
	#get google search's top numLinks ranked links for the topic
	def getLinks(self):
		params = {
		  'api_key': self.api_key,
		  'q': self.topic,
		  'hl': 'en'
		}

		#get google search query response
		apiResult = requests.get('https://api.scaleserp.com/search', params)
		jsonResult = apiResult.json()
		links = []

		#get numLinks links
		for i in range(self.numLinks):
			links.append(jsonResult['organic_results'][i]['link'])

		return links

	#extract text from each link
	def extractText(self, link):
		html = requests.get(link).text
		soup = BeautifulSoup(html, 'html.parser')
		paragraphs = soup.find_all('p')
		text = ' '.join([p.text for p in paragraphs]) #combine all the paragraph tags into one string
		
		#clean up the string
		text = re.sub(r'\[[0-9]*\]', ' ', text)
		text = re.sub(r'\s+', ' ', text)

		return text