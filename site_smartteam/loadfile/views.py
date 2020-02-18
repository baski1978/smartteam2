from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    values = []
    values = getValues('empdetails.csv')
    return render(request, 'empdetails.html',{'emplist':values})


def getValues(filename):
    file=open(filename,'r')
    values = []
    for line in file:
        values.append(line)
    return values