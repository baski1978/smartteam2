from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
import logging
from django import template
from django.template.defaultfilters import stringfilter
from loadfile.models import Individuals
from loadfile.models import IndConsidered
from loadfile.models import Prjnumbers
from loadfile.models import TempTeam
from datetime import datetime
from django.db.models import Avg
from django.db.models import Max
from django.db.models import Count
import random
from site_smartteam.settings import CSVFILES_FOLDER
from django.db.models import Q

#def justcheck(a):
#    return a
########### select random ten people for project #####################

#def getteamindividuals(cnt , skillfilt):
#
#
#	randlist = []
#	randlist3 = []
#	randlist4 = []
#
#	excludids=IndConsidered.objects.values_list('indId',flat=True)
#	if skillfilt=='':
#		randlist = list(Individuals.objects.exclude(Q(indId__in=excludids)).values_list('indId',flat=True))
#	else:
#		randlist = Individuals.objects.exclude(Q(indId__in=excludids)).values_list('indId',flat=True)
#		randlist = list(randlist.filter(Q(indSkill__in =list(skillfilt) )))
#		logging.warning("randlist :oooo: " + str(skillfilt))

#	randlist2 = random.sample(randlist, cnt)
#	x= justcheck(1)
#
#	for i in randlist2:
#		randlist3.append("".join(str(i)).replace(",)",""))
#	for i in randlist3:
#		randlist4.append("".join(str(i)).replace("(",""))
#
#	return list(randlist4)
#
########### crossover defination #####################
#def crossover():
#	Id=TempTeam.objects.values_list('indId',flat=True)
#	popularskillIds = getPopularSkill(Id)
#	popularskillvalue=Individuals.objects.filter(Q(indId__in = popularskillIds)).values_list('indSkill',flat=True)[:1]
#	logging.warning("popularskillvalue is $$$$$$$***#### : " + str(popularskillIds) + ":" + str(popularskillvalue) + ":" + str(Id))
#	indsConsidered=TempTeam.objects.exclude(indId__in=popularskillIds).values_list('indId',flat=True)
#	for x in indsConsidered:
#			prjno=IndConsidered()
#			prjno.indId=x
#			prjno.save()
#
#	TempTeam.objects.filter(Q(indId__in=indsConsidered)).delete()
#	ct = TempTeam.objects.count()
#	crossoverIds=getteamindividuals(10-ct,popularskillvalue)
#	populatetemtable(crossoverIds)

########### mutation defination #####################

#def mutation():
#	
#	tempids = TempTeam.objects.values_list('indId',flat=True)
#	ind28Ids = Individuals.objects.filter(Q(indGrade=28)).filter(indId__in=tempids).values_list('indId',flat=True)
#	if len(ind28Ids)>2:
#		for x in ind28Ids[2:]:
#			prjno=IndConsidered()
#			prjno.indId=x
#			prjno.save()
#		mutationIds=getteamindividuals(len(ind28Ids)-2,'fullstack')
#		populatetemtable(mutationIds)
#	elif len(ind28Ids)==2:
#		pass
#	elif len(ind28Ids)==1:
#		for x in tempids[9:]:
#			prjno=IndConsidered()
#			prjno.indId=x
#			prjno.save()
#		mutationIds=getteamindividuals(1,'fullstack')
#		populatetemtable(mutationIds)
#	elif len(ind28Ids)==0:
#		for x in tempids[8:]:
#			prjno=IndConsidered()
#			prjno.indId=x
#			prjno.save()
#		mutationIds=getteamindividuals(2,'fullstack')
#		populatetemtable(mutationIds) 
#
			
########### Readfile to return file records as as list #####################
#def getValues(filename):
#	values = []
#	try:
#		file=open(filename,'r')
#		next(file)
#		for line in file:
#			values.append(line.replace('\n',''))
#		return values
#	except OSError as err:
#		print("OS error: {0}".format(err))
#	except ValueError:
#		print("Could not convert data to an integer.")
#	except:
#		print("Unexpected error:", sys.exc_info()[0])
#		raise
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
#def countofrecords():
#	ct = Individuals.objects.count()
#	return ct

############ Populate Project table for fitness ###############

#def populatetemtable(tempteam):
#	idlist=[]
#
#	prjno=Prjnumbers()
#	prjno.tag='prj'
#	prjno.save()
#	projectnumber = Prjnumbers.objects.values_list('prjID', flat=True).last()
#
#	for x in tempteam:
#		idlist.append(x)
#
#	tdevopsRatio=gettdevopsRatio(idlist)
#	tdesignRatio=gettdesignRatio(idlist)
#	tavgCost=gettavgCost(idlist)
#	tOnOffRatio=gettOnOffRatio(idlist)
#	tratioGtAvgExp=gettratioGtAvgExp(idlist)
#	tAvgNoOfPto=gettAvgNoOfPto(idlist)
#	tAvgSkillLevel=gettAvgSkillLevel(idlist)
#	tCntdistinctskills=gettCntdistinctskills(idlist)
#	tFitnessValue= gettFitnessValue(tdevopsRatio,tdesignRatio,tavgCost,tOnOffRatio,\
#								 tratioGtAvgExp,tAvgNoOfPto,tAvgSkillLevel,tCntdistinctskills,)
#
#
#
#	for x in tempteam:
#		temp=TempTeam()
#		temp.tname=projectnumber
#		temp.indId= x
#		temp.tdevopsRatio=tdevopsRatio
#		temp.tdesignRatio= tdesignRatio
#		temp.tavgCost=tavgCost['indCost__avg']
#		temp.tOnOffRatio=  tOnOffRatio
#		temp.tratioGtAvgExp=  tratioGtAvgExp['indExp__avg']
#		temp.tAvgNoOfPto  = tAvgNoOfPto['indNoPto__avg']
#		temp.tAvgSkillLevel  = tAvgSkillLevel['indSkillLevel__avg']
#		temp.tCntdistinctskills  = tCntdistinctskills
#		temp.tFitnessValue  = tFitnessValue 	
#		temp.save()

#def getPopularSkill(Id):
#	most_common = Individuals.objects.filter(indId__in=Id).filter(~Q(indRole='domain')).annotate(mc=Count('indSkill')).order_by('-mc')[:1]
#	mostcommonskill= most_common.values_list('indSkill',flat=True)
#	popularskillIds = Individuals.objects.filter(indId__in=Id).filter(indSkill__in=mostcommonskill).values_list('indId',flat=True)
#	return popularskillIds

def gettdevopsRatio(Id):
	try:
		return 100*Individuals.objects.filter(indRole='devops').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()
	except:
		return 0
def gettdesignRatio(Id):
	try:
		return 100*Individuals.objects.filter(indRole='design').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()
	except:
		return 0
def gettavgCost(Id):
	try:
		return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indCost'))
	except:
		return 0
def gettOnOffRatio(Id):
	try:
		return 100*Individuals.objects.filter(indRole='off').filter(indId__in=Id).count()/Individuals.objects.filter(indId__in=Id).count()
	except:
		return 0
def gettratioGtAvgExp(Id):
	try:
		return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indExp'))
	except:
		return 0
def gettAvgNoOfPto(Id):
	return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indNoPto'))

def gettAvgSkillLevel(Id):
		return Individuals.objects.filter(indId__in=Id).aggregate(Avg('indSkillLevel'))

def gettCntdistinctskills(Id):
		return Individuals.objects.filter(indId__in=Id).filter(indGrade__lte=28).values('indSkill').distinct().count()

def gettFitnessValue(tdevopsRatio,tdesignRatio,tavgCost,tOnOffRatio,\
								 tratioGtAvgExp,tAvgNoOfPto,tAvgSkillLevel,tCntdistinctskills,):
	i=0
	try:
		if tdevopsRatio == 50:
			i=i+1
		if tdesignRatio == 30:
			i=i+1
		if tavgCost['indCost__avg'] >=60 and tavgCost['indCost__avg'] <=70:
			i=i+1
		if tOnOffRatio == 90:
			i=i+1
		if tratioGtAvgExp['indExp__avg'] >=4 and tratioGtAvgExp['indExp__avg']<=6:
			i=i+1
		if tAvgSkillLevel['indSkillLevel__avg'] >=2.5 and tAvgSkillLevel['indSkillLevel__avg'] <=5:
			i=i+1
		if tCntdistinctskills <=5:
			i=i+1	
		i= i/7
		return str("{:%}".format(i))
#		if(	tdevopsRatio == 50 and \
#			tdesignRatio ==30 and \
#			tavgCost['indCost__avg'] >=60 and tavgCost['indCost__avg'] <=70  and \
#			tOnOffRatio == 90 and \
#			tratioGtAvgExp['indExp__avg'] >=4 and tratioGtAvgExp['indExp__avg']<=6 and \
#			tAvgNoOfPto['indNoPto__avg'] <= 20 and \
#			tAvgSkillLevel['indSkillLevel__avg'] >=2.5 and tAvgSkillLevel['indSkillLevel__avg'] <=5 and \
#			tCntdistinctskills == 1 ) :
#			return "fit" + " : " + str("{:2f}".format(i))
#		else :
#			return "not fit" + " : " + str("{:%}".format(i))

	except:
		return "not fit 0%"
