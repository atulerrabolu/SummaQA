from flask import Flask, render_template, request
from transformers import BertTokenizer, BertForQuestionAnswering
from modules.summarizer import Summarizer
import torch

app = Flask(__name__)
model = torch.load('./modelweights.pth') #load pretrained BERT Q and A model weights
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		topic = request.form['topic']
		questionsString = request.form['questions']
		questionsList = questionsString.split('\r\n') #split the questions input into a list of each question

		'''get the summary based on questions over the topic that the ML model 
		   finds the answers to through the information found in the top 5 google search link rankings'''
		summary = Summarizer(topic=topic, 
		 					 numLinks=5, 
		 					 questionsList=questionsList, 
		 					 api_key='A14190CA14CA477CAC0ADEE153EB113D',
		 					 model=model,
		 					 tokenizer=tokenizer).getSummary()

		return render_template('index.html', summary=summary)
	else:
		return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)