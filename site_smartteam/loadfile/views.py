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

	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails.html',{'emplist':values,'ctrec':countofrecords(),'data_code':fint })

def projectteams(request):
	#values = []
	#clos =[]
	#values = getValues('/home/nsrivin/dir_smartteam/env_smartteam/site_smartteam/loadfile/empdetails.csv')
	#values = getValues('C:/Users/Admin/source/repos/smartteam2/site_smartteam/loadfile/empdetails.csv')
	#Individuals.objects.all().delete()
	#for rows in values:
	#	cols = rows.split(",")
	#	CreateInd(cols)
	#
	#fint=Team.objects.filter.all()	
	#return render(request, 'projectteams.html',{'emplist':values,'ctrec':countofrecords(),'data_code':fint })
	return render(request, 'projectteams.html')

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
	emp.indTname		   = ind[1]
	emp.indExp             = ind[2]
	emp.indCost            = ind[3]
	emp.indSite            = ind[4]
	emp.indRole            = ind[5]
	emp.indOnoroff         = ind[6]
	emp.indThxNotesG       = ind[7]
	emp.indThxNotesR       = ind[8]
	emp.indGrade           = ind[9]
	emp.indNoPto           = ind[10]
	emp.indDoj             = datetime.strptime("2020/02/20", "%Y/%m/%d")	
	emp.indSkillLevel      = ind[12]
	emp.indSkill           = ind[13]
	emp.save()

def countofrecords():
	ct = Individuals.objects.count()
	return ct
