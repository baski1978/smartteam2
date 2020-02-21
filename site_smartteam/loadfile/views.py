from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import sys
from django import template
from django.template.defaultfilters import stringfilter
from loadfile.models import Individuals
from loadfile.models import TempTeam
from datetime import datetime
from django.db.models import Avg
import random
from settings import CSVFILES_FOLDER



# Create your views here.
########### Home Page#####################
def home(request):
	values = []
	clos =[]
	rowsx = []
	values = getValues(CSVFILES_FOLDER+'empdetails.csv')
	#values = getValues('C:/Users/Admin/source/repos/smartteam2/site_smartteam/loadfile/empdetails.csv')
	Individuals.objects.all().delete()

	for rowsx in values:
		cols = rowsx.split(",")
		CreateInd(cols)

	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails.html',{'emplist':values,'ctrec':countofrecords(),'data_code':fint })

########### select random ten people for project #####################
def projectteams(request):

	randomlist = []
	qindex = Individuals.objects.all()	
	randlist = random.sample(range(qindex.count()), 10)
	randomteam = []

	for i in randlist:
		randomteam.append(qindex[i])
	TempTeam.objects.all().delete()
	populatetemtable(randomteam)
	fint=TempTeam.objects.all()	

	return render(request, 'projectteams.html',{'data_code':fint})

########### Readfile to return file records as as list #####################
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

########### Readfile to retunr file records as as list #####################
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

############ Get count of records for Individuals table ###############
def countofrecords():
	ct = Individuals.objects.count()
	return ct

############ Populate Project table for fitness ###############

def populatetemtable(tempteam):
	idlist=[]
	for x in tempteam:
		idlist.append(x.indId)
	tdevopsRatio=gettdevopsRatio(idlist)
	tdesignRatio=gettdesignRatio(tempteam)
	tavgTenure=gettavgTenure(tempteam)
	tOnOffRatio=gettOnOffRatio(tempteam)
	tratioGtAvgExp=gettratioGtAvgExp(tempteam)
#	tpctThxNotesG=gettpctThxNotesG(tempteam)
#	tpctThxNotesR=gettpctThxNotesR(tempteam)
#	tAvgDurationBygrade=gettAvgDurationBygrade(tempteam)
#	tpctGdurationGtAvgduration=gettpctGdurationGtAvgduration(tempteam)
#	tAvgNoOfPto=gettAvgNoOfPto(tempteam)
#	tPctPepleGtAvgpto=gettPctPepleGtAvgpto(tempteam)
#	tPctSameJdate=gettPctSameJdate(tempteam)
#	tFitnessValue=gettFitnessValue(tempteam)

	for x in tempteam:
		temp=TempTeam()
		temp.tname=x.indTname
		temp.indId=x.indId
		temp.tdevopsRatio=tdevopsRatio
		temp.tdesignRatio= tdesignRatio
		temp.tavgTenure=tratioGtAvgExp
		temp.tOnOffRatio=  tOnOffRatio
		temp.tratioGtAvgExp=  tratioGtAvgExp
		temp.tpctThxNotesG= '123' # tpctThxNotesG
		temp.tpctThxNotesR= '123' # tpctThxNotesR
		temp.tAvgDurationBygrade= '123' # tAvgDurationBygrade
		temp.tpctGdurationGtAvgduration= '123' # tpctGdurationGtAvgduration
		temp.tAvgNoOfPto= '123' # tAvgNoOfPto
		temp.tPctPepleGtAvgpto= '123' # tPctPepleGtAvgpto
		temp.tPctSameJdate= '123' # tPctSameJdate
		temp.tFitnessValue= '123' # tFitnessValue
		temp.save()

def gettdevopsRatio(Id):
	return 100*Individuals.objects.filter(indRole='devops').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()

def gettdesignRatio(Id):
	return 100*Individuals.objects.filter(indRole='design').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()

def gettOnOffRatio(tempteam):
	return 100*Individuals.objects.filter(indRole='off').filter(indId__in=Id).count()/Individuals.objects.filter(indRole='on').filter(indId__in=Id).count()

def gettratioGtAvgExp(tempteam):
	return Individuals.objects.filter(indId__in=Id).aggregate(Avg(indExp))
#def gettpctThxNotesG(tempteam)
#def gettpctThxNotesR(tempteam)
#def gettAvgDurationBygrade(tempteam)
#def gettpctGdurationGtAvgduration(tempteam)
#def gettAvgNoOfPto(tempteam)
#def gettPctPepleGtAvgpto(tempteam)
#def gettPctSameJdate(tempteam)
#def gettFitnessValue(tempteam)

#calculatefitness

#crossover with bench

#mutate from bench

#calculatefitness

#if fitness=10 then comiit the team delete from bench and add to prjoect teams
#else
#go to crossover with bench



