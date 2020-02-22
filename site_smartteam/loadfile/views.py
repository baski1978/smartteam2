from django.shortcuts import render
from django.http import HttpResponse
import os
#from django.conf import site_smartteam.settings
import sys
from django import template
from django.template.defaultfilters import stringfilter
from loadfile.models import Individuals
from loadfile.models import IndConsidered
from loadfile.models import Prjnumbers
from loadfile.models import TempTeam
from datetime import datetime
from django.db.models import Avg
from django.db.models import Max
import random
from site_smartteam.settings import CSVFILES_FOLDER
from django.db.models import Q



# Create your views here.
########### em details Page#####################
def home(request):
	values = []
	clos =[]
	rowsx = []
	values = getValues(CSVFILES_FOLDER+'empdetails.csv')
	Individuals.objects.all().delete()

	for rowsx in values:
		cols = rowsx.split(",")
		CreateInd(cols)

	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails2.html',{'emplist':values,'ctrec':countofrecords(),'data_code':fint })

########### select random ten people for project #####################

def getteamindividuals(cnt):

	randomlist = []
	qindex = Individuals.objects.all() #exclude(indId__in=IndConsidered.objects.all().values('indId'))	
	randlist = random.sample(range(qindex.count()), cnt)
	randomteam = []

	for i in randlist:
		randomteam.append(qindex[i])
	return randomteam
	


########### Render the project team page #####################

def projectteams(request):

	randomteam=getteamindividuals(10)
	TempTeam.objects.all().delete()
	populatetemtable(randomteam)
	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]

	while fitvalue != 'fit':
		randomteam=getteamindividuals(8)
		for x in TempTeam.objects.values_list('indId',flat=True)[:8]:
			prjno=IndConsidered()
			prjno.indId=x
			prjno.save()
			TempTeam.objects.filter(indId=x).delete()
		for x in TempTeam.objects.values_list('indId',flat=True)[:2]:
			randomteam.append(x)
			TempTeam.objects.filter(indId=x).delete()
		populatetemtable(randomteam)
		fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]	

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

	prjno=Prjnumbers()
	prjno.tag='prj'
	prjno.save()
	projectnumber = Prjnumbers.objects.values_list('prjID', flat=True).last()

	for x in tempteam:
		idlist.append(x.indId)

	tdevopsRatio=gettdevopsRatio(idlist)
	tdesignRatio=gettdesignRatio(idlist)
	tavgCost=gettavgCost(idlist)
	tOnOffRatio=gettOnOffRatio(idlist)
	tratioGtAvgExp=gettratioGtAvgExp(idlist)
	tAvgNoOfPto=gettAvgNoOfPto(idlist)
	tAvgSkillLevel=gettAvgSkillLevel(idlist)
	tCntdistinctskills=gettCntdistinctskills(idlist)
	tFitnessValue= gettFitnessValue(tdevopsRatio,tdesignRatio,tavgCost,tOnOffRatio,\
								 tratioGtAvgExp,tAvgNoOfPto,tAvgSkillLevel,tCntdistinctskills,)



	for x in tempteam:
		temp=TempTeam()
		temp.tname=projectnumber
		temp.indId= x.indId
		temp.tdevopsRatio=tdevopsRatio
		temp.tdesignRatio= tdesignRatio
		temp.tavgCost=tavgCost['indCost__avg']
		temp.tOnOffRatio=  tOnOffRatio
		temp.tratioGtAvgExp=  tratioGtAvgExp['indExp__avg']
		temp.tAvgNoOfPto  = tAvgNoOfPto['indNoPto__avg']
		temp.tAvgSkillLevel  = tAvgSkillLevel['indSkillLevel__avg']
		temp.tCntdistinctskills  = tCntdistinctskills
		temp.tFitnessValue  = tFitnessValue 	
		temp.save()


def gettdevopsRatio(Id):
	return 100*Individuals.objects.filter(indRole='devops').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()

def gettdesignRatio(Id):
	return 100*Individuals.objects.filter(indRole='design').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()

def gettavgCost(Id):
	return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indCost'))

def gettOnOffRatio(Id):
	return 100*Individuals.objects.filter(indRole='off').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()

def gettratioGtAvgExp(Id):
	return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indExp'))

def gettAvgNoOfPto(Id):
	return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indNoPto'))

def gettAvgSkillLevel(Id):
		return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indSkillLevel'))

def gettCntdistinctskills(Id):
		return Individuals.objects.filter(indId__in=Id).filter(indGrade__lte=28).values('indSkill').distinct().count()

def gettFitnessValue(tdevopsRatio,tdesignRatio,tavgCost,tOnOffRatio,\
								 tratioGtAvgExp,tAvgNoOfPto,tAvgSkillLevel,tCntdistinctskills,):
	if(	tdevopsRatio == 50 and \
		tdesignRatio ==30 and \
		tavgCost >=60 and tavgCost <=70  and \
		tOnOffRatio == 90 and \
		tratioGtAvgExp >=4 and tratioGtAvgExp<=6 and \
		tAvgNoOfPto <= 20 and \
		tAvgSkillLevel >=2.5 and tAvgSkillLevel <=5 and \
		tCntdistinctskills == 1 ) :
		return "fit"
	else :
		return "not fit"




