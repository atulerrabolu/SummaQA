import torch

#code modified from Chris McCormick's BERT tutorial
class ModelQA:
	def __init__(self, questionList, source, model, tokenizer):
		self.questionList = questionList
		self.source = source
		self.model = model
		self.tokenizer = tokenizer

	def getAnswers(self):
		answerList = []

		#find answer for each question
		for qIdx in range(len(self.questionList)):
			question = self.questionList[qIdx]

			#tokenize and encode the input
			inputIds = self.tokenizer.encode(question, self.source, max_length=512)
			tokens = self.tokenizer.convert_ids_to_tokens(inputIds)

			#add token type ids to differentiate between question and source text
			sepTokenIdx = inputIds.index(self.tokenizer.sep_token_id)
			questionSegmentLen = sepTokenIdx + 1
			sourceSegmentLen = len(inputIds) - questionSegmentLen
			tokenTypeIds = [0]*questionSegmentLen + [1]*sourceSegmentLen
			answer = ''

			#feed input into model
			outputs = self.model(torch.tensor([inputIds]),
							 	 token_type_ids=torch.tensor([tokenTypeIds]))

			#take the start and end word in the answer sequence with highest probability
			startScores = outputs.start_logits
			endScores = outputs.end_logits
			startIdx = torch.argmax(startScores)
			endIdx = torch.argmax(endScores)

			#do some string formatting to merge subwords
			answer = tokens[startIdx]

			for i in range(startIdx + 1, endIdx + 1):
			    if tokens[i][0:2] == '##':
			        answer += tokens[i][2:]
			    else:
			        answer += ' ' + tokens[i]
			
			if '[CLS]' in answer or '[SEP]' in answer:
				answerList.append('N/A')
			else:
				answerList.append(answer)

		return answerList