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

def home(request):
	IndConsidered.objects.all().delete()
	return render(request, 'index.html')

def empdetails(request):
	values = []
	clos =[]
	rowsx = []
	
	values = getValues(CSVFILES_FOLDER+'empdetails.csv') 
	Individuals.objects.all().delete()
	IndConsidered.objects.all().delete()
	TempTeam.objects.all().delete()
	Prjnumbers.objects.all().delete()
	for rowsx in values:
		cols = rowsx.split(",")
		CreateInd(cols)
	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails2.html',{'emplist':values,'ctrec':countofrecords(),'data_emp':fint })

def CommitTeam(request,prjno):

	IndConsidered.objects.all().delete()
	TempTeam.objects.all().delete()
	Prjnumbers.objects.all().delete()
	Id=TempTeam.objects.values_list('indId',flat=True)

	for rowsx in values:
		cols = rowsx.split(",")
		CreateInd(cols)
	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails2.html',{'emplist':values,'ctrec':countofrecords(),'data_emp':fint })


def projectteams(request, indIdno):
	
	if indIdno==0:
		TempTeam.objects.all().delete()
		IndConsidered.objects.all().delete()
		a=[]
		prjno=populatetemtable2(10,a,'')

	fitvalue=str(TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]).replace("<QuerySet ['","").replace("']>","")
	popularskillids , popularskill = mostpopularskill()
	logging.warning("fitvalue,fitvalue,fitvalue,fitvalue,fitvalue,fitvalue"+str(fitvalue))

	crossover2(popularskillids,popularskill,prjno)									  			    #step3: Do Crossover & mutation 
	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]

	fint=TempTeam.objects.all().order_by('indId')																#step7: Get project details
	currentteamids=TempTeam.objects.values_list('indId',flat=True)            
	indIdnodetails=Individuals.objects.filter(Q(indId__in=currentteamids)).all().order_by('indId','indGrade')				#step8: Get Individual details
	return render(request, 'projectteams.html',{'data_prj':fint , 'data_ind':indIdnodetails})	#Step9: Display
		
def	populatetemtable2(cnt,crossoverIds,prjno):																#Step1: Pick random teams

	if cnt==5000:		
		currentteamids=TempTeam.objects.values_list('indId',flat=True)  
		currentteamids=str(currentteamids).replace("<QuerySet [","").replace("]>","").split(",") #replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
		tempteamids=crossoverIds+currentteamids
	else:
		ids28=getteamindividuals_28(2,"")
		idsn28=getteamindividuals_n28(8,"")
		tempteamids=ids28+idsn28
	if prjno=='':
		prjno=Prjnumbers()
		prjno.tag='prj'
		prjno.save()
		projectnumber = Prjnumbers.objects.values_list('prjID', flat=True).last()
	else:
	   projectnumber=prjno

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
	TempTeam.objects.all().delete()
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
	return projectnumber	


################ crossover defination #####################
def crossover2(popularskillIds,popularskillvalue,prjno):	
	cursor = connection.cursor()
	if popularskillvalue=="":
		return
	else:
		qstr="select indId from  loadfile_Individuals where IndGrade!='28' and ( indSkill != 'fullstack' and indSkill !='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' ) and indId  in ( select indId from  loadfile_TempTeam)"
		cursor.execute(qstr)
		row = cursor.fetchall()
		row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
		cursor.close()
		if str(row)=='':
			return
		else:	
			ct=indConsidered(row)
			crossoverIds=getteamindividuals_n28(ct,popularskillvalue)
			populatetemtable2(5000,crossoverIds,prjno)
	#logging.warning("crossoverIdscrossoverIdscrossoverIdscrossoverIds:"+str(crossoverIds))
	mutation2(popularskillvalue,prjno)
	pass

def mutation2(popularskillvalue,prjno):
	cursor = connection.cursor()
	qstr="select indId from  loadfile_Individuals where indGrade ='28' and ( indSkill != 'fullstack' and indSkill!='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' ) and indId  in ( select indId from  loadfile_TempTeam)"
	cursor.execute(qstr)	
	row=cursor.fetchall()
	row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
	cursor.close()
	if str(row)=='':
		return
	else:
		#logging.warning("mutation2mutation2mutation2mutation2mutation2:"+str(row))
		ct=indConsidered(row)
		MutionIds=getteamindividuals_28(ct,popularskillvalue)
		populatetemtable2(5000,MutionIds,prjno)

def mostpopularskill():
	Id=TempTeam.objects.values_list('indId',flat=True)
	most_common = Individuals.objects.filter(indId__in=Id).filter(~Q(indRole='domain')).annotate(mc=Count('indSkill')).order_by('-mc')[:1]
	mostcommonskill= most_common.values_list('indSkill',flat=True)
	popularskillIds = Individuals.objects.filter(Q(indId__in=Id)).filter(Q(indSkill__in=mostcommonskill)).values_list('indId',flat=True)
	popularskillvalue=Individuals.objects.filter(Q(indId__in = popularskillIds)).values_list('indSkill',flat=True)[:1]	
	return popularskillIds , popularskillvalue
	
def get28ids():
	g28Ids=Individuals.objects.filter(indGrade='28').values_list('indId',flat=True)
	tem28id=TempTeam.objects.filter(indId__in=g28Ids).values_list('indId',flat=True)
	return tem28id

def indConsidered(indsConsidered):
	try:
		ct=0
		#logging.warning("uuuuuuuuuuuuuuuuuuuuuuuu:llllllllll:"+str(indsConsidered))
		for x in indsConsidered:
			prjno=IndConsidered()
			prjno.indId=x
			prjno.save()
			ct=ct+1
		TempTeam.objects.filter(Q(indId__in=indsConsidered)).delete()
		return ct
	except:
		return 0
def getteamindividuals_28(cnt,popularskillvalue):
		cursor = connection.cursor()
		if popularskillvalue=="":
			cursor.execute( "select indId from  loadfile_Individuals where indGrade =='28'  and indId not in ( select indId from  loadfile_IndConsidered)")
		else:
			qstr="select indId from  loadfile_Individuals where indGrade =='28' and ( indSkill = 'fullstack' or indSkill='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' ) and indId not in ( select indId from  loadfile_IndConsidered)"
			cursor.execute(qstr)
		row = cursor.fetchall()
		row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").split(",")
		cursor.close()
		randlist = random.sample(row, cnt)
		return randlist

def getteamindividuals_n28(cnt,popularskillvalue):
		cursor = connection.cursor()
		if popularskillvalue=="":
			cursor.execute( "select indId from  loadfile_Individuals where indGrade !='28' and indId not in ( select indId from  loadfile_IndConsidered)")
		else:
			qstr="select indId from  loadfile_Individuals where indGrade !='28' and indSkill='" + str(popularskillvalue).replace("<QuerySet ['","").replace("']>","") + "' and indId not in ( select indId from  loadfile_IndConsidered)"
			#logging.warning(str(popularskillvalue)+"MMMMMMMMMMMMMMMMMASDSADASDERRWRWEREWRWER")
			cursor.execute(qstr)
		row = cursor.fetchall()
		row=str(row).replace("[","").replace("]","").replace("(","").replace(",)","").split(",")
		cursor.close()
		randlist = random.sample(row, cnt)
		return randlist