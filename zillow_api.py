import requests
from xml.etree import ElementTree
import urllib2
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import mysql.connector

DB_NAME = 'yelp_zillow'

URLS = ['http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Tempe',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Phoenix',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Scottsdale',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Chandler',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Laveen',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Goodyear',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Buckeye',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Glendale',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Peoria',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Gilbert',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Mesa',
	   'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Tolleson']
CITIES = ['Tempe', 'Phoenix', 'Scottsdale', 'Chandler', 'Laveen', 'Goodyear', 'Buckeye', 'Glendale', 'Peoria', 'Gilbert', 'Mesa', 'Tolleson']

tags_for_Median_Home_val = ['pages', 'page', 'tables', 'table', 'data', 'attribute', 'values', 'city', 'value']
tags_for_Median_income = ['pages', 'page', 'tables', 'table', 'data', 'attribute', 'values', 'city', 'value']
tags_for_single_male = ['pages', 'page']
def get_median_income(data):
	Median_income = parseString(data)
	for tag in tags_for_Median_income:
		if tag == 'page':
			Median_income = Median_income.getElementsByTagName(tag)[2].toxml()
			Median_income = parseString(Median_income)
		else:
			Median_income = Median_income.getElementsByTagName(tag)[0].toxml()
			if tag != "value":
				Median_income = parseString(Median_income)
	Median_income = str( Median_income.replace('<value currency="USD">', '').replace('</value>', '') )
	return Median_income

def get_med_houseVal(data):
	dom = parseString(data)
	for tag in tags_for_Median_Home_val:
		Median_Home_Val = dom.getElementsByTagName(tag)[0].toxml()
	Median_Home_Val= str(Median_Home_Val.replace('<value type="USD">', '').replace('</value>', ''))
	return Median_Home_Val

def get_api_responses(urls):
	api_responses = []
	for url in urls:
		file = urllib2.urlopen(url)
		data = file.read()
		file.close()
		api_responses.append(data)
	return api_responses

def get_single_male(data):
	fo = open("foo.xml","w+")
	fo.write(data)
	fo.close()

	tree = ET.parse("foo.xml")
	root = tree.getroot()
	root = root[2]
	root = root[4]
	root = root[2]
	root = root[1]
	root = root[0]
	root = root [1]
	root = root[1]
	root = root[1] 
	return root[0][0].text

def get_single_female(data):
	fo = open("foo.xml","w+")
	fo.write(data)
	fo.close()

	tree = ET.parse("foo.xml")
	root = tree.getroot()
	root = root[2]
	root = root[4]
	root = root[2]
	root = root[1]
	root = root[0]
	root = root [1]
	root = root[2]
	root = root[1] 
	return root[0][0].text

def get_rent_percent(data):
	fo = open("foo.xml","w+")
	fo.write(data)
	fo.close()

	tree = ET.parse("foo.xml")
	root = tree.getroot()
	root = root[2][4][1][1][0][1][1][1][0][0]
	# This would get me national avg root = root[2][4][1][1][0][1][1][1][1][0]
	return root.text

def get_homes_wKids(data):
	fo = open("foo.xml","w+")
	fo.write(data)
	fo.close()

	tree = ET.parse("foo.xml")
	root = tree.getroot()
	root = root[2][4][2][1][0][1][4][1][0][0]
	return root.text

api_responses = get_api_responses(URLS)

cnx = mysql.connector.connect(user='root', database=DB_NAME)
cursor = cnx.cursor()

add_city = ("INSERT INTO zillow (cityName, singleMale, singleFemale, homePrice, singleHomes, rentPercent, avgIncome) VALUES (%s, %s, %s, %s, %s, %s, %s)")
for name, data in zip(CITIES, api_responses):
	sMale = get_single_male(data)
	sFemale = get_single_female(data)
	homeP = get_med_houseVal(data)
	sHomes = get_homes_wKids(data)
	rent = get_rent_percent(data)
	medIncome = get_median_income(data)
	city_data = (name, sMale, sFemale, homeP, sHomes, rent, medIncome)
	cursor.execute(add_city, city_data)
	cnx.commit()
cursor.close()
cnx.close()


