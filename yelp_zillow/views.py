import mysql.connector
from django.shortcuts import render
import datetime
from django.http import HttpResponse
from django.template import Template
from sprocs import yelp_table, zillow_table

def home(request):
    return render(request, 'bare.html')

def search(request):
	if request.POST:
		city = str(request.POST.get('city'))
		restaurants, ratings = yelp_table.get_restaurants(city)
		sMale, sFemale, homPrice, singleHome, rentPer, averageIncome = zillow_table.get_data(city)
		