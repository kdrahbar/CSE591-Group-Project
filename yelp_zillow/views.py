from django.shortcuts import render
import datetime
from django.http import HttpResponse
from django.template import Template

def home(request):
    return render(request, 'bare.html')