from django.shortcuts import render
from django.http import HttpResponse
import os
import sys
from django import template
from utils.functions2 import *






# Create your views here.
########### em details Page#####################
def home(request):
	IndConsidered.objects.all().delete()
	return render(request, 'index.html')

def empdetails(request):
	values = []
	clos =[]
	rowsx = []
	
	fint=Individuals.objects.filter(indTname='bench').all()	
	return render(request, 'empdetails2.html',{'emplist':values,'ctrec':countofrecords(),'data_emp':fint })

	


########### Render the project team page #####################

def projectteams(request, indIdno):


	randomteam=getteamindividuals(10,'')
	TempTeam.objects.all().delete()
	Prjnumbers.objects.all().delete()
	populatetemtable(randomteam)
	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]
	
#	while fitvalue != 'fit':
	crossover()	
	#aftercrossover=TempTeam.objects.all()	
	mutation()
	#aftermutation=TempTeam.objects.all()	
	fitvalue=TempTeam.objects.values_list('tFitnessValue',flat=True)[:1]
	fint=TempTeam.objects.all()	
	currentteamids=TempTeam.objects.values_list('indId',flat=True)
	firstid=TempTeam.objects.values_list('indId',flat=True)[:1]
	
	indIdnodetails=Individuals.objects.filter(Q(indId__in=currentteamids)).all()
	#return render(request, 'projectteams.html',{'data_prj':fint, 'idno':firstid})
	return render(request, 'projectteams.html',{'data_prj':fint , 'data_ind':indIdnodetails})

		





