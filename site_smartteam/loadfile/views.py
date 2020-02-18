from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import sys
from django import template
from django.template.defaultfilters import stringfilter



# Create your views here.
def home(request):
	values = []
	values = getValues('/home/nsrivin/dir_smartteam/env_smartteam/site_smartteam/loadfile/empdetails.csv')
	return render(request, 'empdetails.html',{'emplist':values})

def funsplit(texts):
	return texts.split(",")

def getValues(filename):
	values = []
	try:
		file=open(filename,'r')
		for line in file:
			values.append(line)
		return values
	except OSError as err:
		print("OS error: {0}".format(err))
	except ValueError:
		print("Could not convert data to an integer.")
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise