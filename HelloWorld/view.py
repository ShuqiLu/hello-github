#from django.http import HttpResponse
from django.shortcuts import render
from neo4j.v1 import GraphDatabase
def hello(request):
	
	context = {}
	context['hello'] = 'kjhkh'
	return render(request, 'hello.html', context)