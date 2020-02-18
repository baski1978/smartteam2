from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
	values[] = getValues('empdetails.csv')
    return render(request, 'empdetails.html',{'emplist':values[]})


def getValues(filename):
	try:
		file=open(filename,'r')
	except IOError:
		print 'problem with file' , filename

	values = []
	for line in file:
		values.append(line)
	return values