from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
from django import template
from utils.functions2 import *
from django.db import *
from loadfile.models import Individuals
from loadfile.models import IndConsidered
from loadfile.models import Prjnumbers
from loadfile.models import TempTeam


# Create your views here.
########### em details Page#####################
def home(request):
	IndConsidered.objects.all().delete()
	return render(request, 'index.html')

def empdetails(request):
	values = []
	clos =[]
	rowsx = []
	
	#values = getValues(CSVFILES_FOLDER+'empdetails.csv')
	#Individuals.objects.all().delete()
	IndConsidered.objects.all().delete()
	TempTeam.objects.all().delete()
	Prjnumbers.objects.all().delete()
	#for rowsx in values:
	#	cols = rowsx.split(",")
	#	CreateInd(cols)
	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails2.html',{'emplist':values,'ctrec':countofrecords(),'data_emp':fint })

	


########### Render the project team page #####################

def projectteams(request, indIdno):
	
	TempTeam.objects.all().delete()
	populatetemtable2(10)
#	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]						#Step2: Check fitvalue	
	
#	while fitvalue != 'fit':
	crossover2()																				#step3: Do Crossover for none28								
#	mutation()																					#Step4: Do Mutation for 28
#	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]						#Step6: Check fit value
	fint=TempTeam.objects.all()																	#step7: Get project details
	currentteamids=TempTeam.objects.values_list('indId',flat=True)            
	indIdnodetails=Individuals.objects.filter(Q(indId__in=currentteamids)).all()				#step8: Get Individual details
	return render(request, 'projectteams.html',{'data_prj':fint , 'data_ind':indIdnodetails})	#Step9: Display
		
def getteamindividuals_28(cnt,popularskillvalue):
		cursor = connection.cursor()
		if popularskillvalue=="":
			cursor.execute( "select indId from  loadfile_Individuals where indGrade =='28'  and indId not in ( select indId from  loadfile_IndConsidered)")
		else:
			qstr="select indId from  loadfile_Individuals where indGrade =='28' and indSkill='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' and indId not in ( select indId from  loadfile_IndConsidered)"
			cursor.execute(qstr)
		row = cursor.fetchall()
		row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
		cursor.close()
		randlist = random.sample(row, cnt)
		return randlist

def getteamindividuals_n28(cnt,popularskillvalue):
		cursor = connection.cursor()
		if popularskillvalue=="":
			cursor.execute( "select indId from  loadfile_Individuals where indGrade !='28' and indId not in ( select indId from  loadfile_IndConsidered)")
		else:
			qstr="select indId from  loadfile_Individuals where indGrade !='28' and indSkill='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' and indId not in ( select indId from  loadfile_IndConsidered)"
			logging.warning(qstr)
			cursor.execute(qstr)
		row = cursor.fetchall()
		row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
		cursor.close()
		randlist = random.sample(row, cnt)
		return randlist
def	populatetemtable2(cnt):																#Step1: Pick random teams
	ids28=getteamindividuals_28(2,"")
	idsn28=getteamindividuals_n28(8,"")
	tempteamids=ids28+idsn28
	prjno=Prjnumbers()
	prjno.tag='prj'
	prjno.save()
	projectnumber = Prjnumbers.objects.values_list('prjID', flat=True).last()

	tdevopsRatio=gettdevopsRatio(tempteamids)
	tdesignRatio=gettdesignRatio(tempteamids)
	tavgCost=gettavgCost(tempteamids)
	tOnOffRatio=gettOnOffRatio(tempteamids)
	tratioGtAvgExp=gettratioGtAvgExp(tempteamids)
	tAvgNoOfPto=gettAvgNoOfPto(tempteamids)
	tAvgSkillLevel=gettAvgSkillLevel(tempteamids)
	tCntdistinctskills=gettCntdistinctskills(tempteamids)
	tFitnessValue= gettFitnessValue(tdevopsRatio,tdesignRatio,tavgCost,tOnOffRatio,\
								 tratioGtAvgExp,tAvgNoOfPto,tAvgSkillLevel,tCntdistinctskills,)
	for x in tempteamids:
		temp=TempTeam()
		temp.tname=projectnumber
		temp.indId= x
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

################ crossover defination #####################
def crossover2():
	Id=TempTeam.objects.values_list('indId',flat=True)
	most_common = Individuals.objects.filter(indId__in=Id).filter(~Q(indRole='domain')).annotate(mc=Count('indSkill')).order_by('-mc')[:1]
	mostcommonskill= most_common.values_list('indSkill',flat=True)
	popularskillIds = Individuals.objects.filter(indId__in=Id).filter(indSkill__in=mostcommonskill).values_list('indId',flat=True)
	popularskillvalue=Individuals.objects.filter(Q(indId__in = popularskillIds)).values_list('indSkill',flat=True)[:1]
	indsConsidered=TempTeam.objects.exclude(indId__in=popularskillIds).values_list('indId',flat=True)
	for x in indsConsidered:
			prjno=IndConsidered()
			prjno.indId=x
			prjno.save()
	TempTeam.objects.filter(Q(indId__in=indsConsidered)).delete()
	ct = TempTeam.objects.count()
	crossoverIds=getteamindividuals_n28(10-ct,popularskillvalue)
	populatetemtable(crossoverIds)
	mutation2(popularskillvalue,Id)

def mutation2(popularskillvalue,Id):

	Ids = Individuals.objects.filter(indId__in=Id).filter('indGrade'=='28' ).filter('indSkill'!=popularskillvalue).filter('indSkill'!='fullstack')
	indsConsidered=TempTeam.objects.exclude(indId__in=Ids).values_list('indId',flat=True)
	ct=0
	for x in indsConsidered:
		prjno=IndConsidered()
		prjno.indId=x
		prjno.save()
		ct=ct+1
	TempTeam.objects.filter(Q(indId__in=indsConsidered)).delete()
	MutionIds=getteamindividuals_28(ct,popularskillvalue)
	populatetemtable(MutionIds)