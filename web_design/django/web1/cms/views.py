from django.shortcuts import render
from django.http import request,HttpResponse
from django.forms.models import model_to_dict
import time
import json
from models import Question
# Create your views here.
def hello(request):
	return HttpResponse("Hello world ! ")

def add_to_model(request):
	if request.method == 'GET':
		question_text = str(request.GET['a'])
		question = Question.objects.all()
		data = []
		for item in question:
			item_data = {}
			item_data['id'] = item.id
			item_data['pub_date'] = item.pub_date
			print(item.pub_date)
			item_data['question_text'] =item.question_text
			data.append(item_data)
		return HttpResponse (data)
