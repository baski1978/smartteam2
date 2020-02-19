from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import sys
from django import template
from django.template.defaultfilters import stringfilter
from loadfile.models import Individuals
from datetime import datetime



# Create your views here.
def home(request):
	values = []
	clos =[]
	values = getValues('/home/nsrivin/dir_smartteam/env_smartteam/site_smartteam/loadfile/empdetails.csv')
	#values = getValues('C:/Users/Admin/source/repos/smartteam2/site_smartteam/loadfile/empdetails.csv')
	Individuals.objects.all().delete()
	for rows in values:
		cols = rows.split(",")
		CreateInd(cols)

	fint=Individuals.objects.all()	
	return render(request, 'empdetails.html',{'emplist':values,'ctrec':countofrecords(),'data_code':fint })

def funsplit(texts):
	return texts.split(",")

def getValues(filename):
	values = []
	try:
		file=open(filename,'r')
		next(file)
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
def deleteobjects():
	Individuals.objects.all().delete()

def CreateInd(ind):
	emp = Individuals()
	emp.indId              = ind[0]
	emp.indTname		   = ind[2]
	emp.indExp             = ind[3]
	emp.indCost            = ind[4]
	emp.indSite            = ind[5]
	emp.indRole            = ind[6]
	emp.indOnoroff         = ind[7]
	emp.indThxNotesG       = ind[8]
	emp.indThxNotesR       = ind[9]
	emp.indGrade           = ind[10]
	emp.indNoPto           = ind[11]
	emp.indDoj             = datetime.strptime("2020/02/20", "%Y/%m/%d")	
	emp.indSkillLevel      = ind[13]
	emp.indSkill           = ind[14]
	emp.save()

def countofrecords():
	ct = Individuals.objects.count()
	return ct
