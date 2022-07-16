
from flask import Flask, render_template, request
from transformers import BertTokenizer, BertForQuestionAnswering
from modules.summarizer import Summarizer
import torch

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
torch.save(model, 'modelweights.pth')
