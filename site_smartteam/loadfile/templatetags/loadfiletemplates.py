from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import sys
from django import template
from django.template.defaultfilters import stringfilter
from django.apps import apps as django_apps

register = template.Library()


@register.filter(name='splitting')
def splitting(value,arg):
	return value.split(arg)
