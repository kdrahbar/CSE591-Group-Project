import requests
from xml.etree import ElementTree
import urllib2
from xml.dom.minidom import parseString

def original_dom(data):
	dom = parseString(data)
	xmlTag = dom.getElementsByTagName('response')[0].toxml()
	xmlData=xmlTag.replace('<response>','').replace('</response>','')
	return xmlData

URL = 'http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Tempe'
#import easy to use xml parser called minidom:
#from xml.dom.minidom import parseString
#r = requests.get('http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1dq74ir953f_8fetn&state=AZ&city=Tempe')
#tree = ElementTree.fromstring(r.content)

tags_for_Median_Home_val = ['pages', 'page', 'tables', 'table', 'data', 'attribute', 'values', 'city', 'value']
tags_for_Median_income = ['pages', 'page', 'tables', 'table', 'data', 'attribute', 'values', 'city', 'value']


file = urllib2.urlopen(URL)
data = file.read()
file.close()
dom = parseString(data)
#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
xmlTag = dom.getElementsByTagName('response')[0].toxml()
#strip off the tag (<tag>data</tag>  --->   data):
xmlData=xmlTag.replace('<response>','').replace('</response>','')

# Retrieve the tag for median home value
Median_Home_Val = original_dom(data)
for tag in tags_for_Median_Home_val:
	Median_Home_Val = dom.getElementsByTagName(tag)[0].toxml()
Median_Home_Val= int(Median_Home_Val.replace('<value type="USD">', '').replace('</value>', ''))

Median_income = parseString(data)
count = 0
for tag in tags_for_Median_income:
	if tag == 'page':
		Median_income = Median_income.getElementsByTagName(tag)[2].toxml()
		Median_income = parseString(Median_income)
	else:
		Median_income = Median_income.getElementsByTagName(tag)[0].toxml()
		if tag != "value":
			Median_income = parseString(Median_income)

		
Median_income = int( Median_income.replace('<value currency="USD">', '').replace('</value>', '') )
print Median_income

