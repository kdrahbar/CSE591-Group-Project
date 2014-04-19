import json
from django.shortcuts import render
import datetime
from django.http import HttpResponse
from django.template import Template
from sprocs import yelp_table, zillow_table
import locale
locale.setlocale( locale.LC_ALL, '' )

LAT = {"Tempe":33.425884,
		"Phoenix":33.451441,
		"Scottsdale":33.492877,
		"Chandler":33.305058,
		"Laveen":33.362454,
		"Goodyear":33.440115,
		"Buckeye":33.372753,
		"Peoria":33.583276,
		"Gilbert":33.353306,
		"Glendale":33.541073,
		"Tolleson":33.450114,
		"Mesa":33.414129}

LONG = {"Tempe":-111.938057,
		"Phoenix":-112.074239,
		"Scottsdale":-111.924372,
		"Chandler":-111.840850,
		"Laveen":-112.170743,
		"Goodyear":-112.395857,
		"Buckeye":-112.604818,
		"Peoria":-112.252272,
		"Gilbert":-111.789025,
		"Glendale":-112.185602,
		"Tolleson":-112.258346,
		"Mesa":-111.829769}

def trunc(f, n):
	f = float(f)
	return ('%.*f' % (n + 1, f))[:-1]
def format(f):
	f = float(f)
	return locale.currency( f, grouping=True )

def home(request):
    return render(request, 'home.html')

def search(request):
	if request.POST:
		city = str(request.POST.get('place'))
		if ',' in city:
			city = city.replace(' ', '')
			places = city.split(',')
			restaurants, ratings, sMale, sFemale, homPrice, singleHome, rentPer, averageIncome, locations = [],[],[],[],[],[],[],[],[]
			for place in places:
				restaurantsT, ratingsT = yelp_table.get_restaurants(place)
				sMale_t, sFemale_t, homPrice_t, singleHome_t, rentPer_t, averageIncome_t = zillow_table.get_data(place)
				locations.append([str(LAT[place]), str(LONG[place])])
				sMale.append(trunc(sMale_t, 3))
				sFemale.append(trunc(sFemale_t, 3))
				homPrice.append(format(homPrice_t))
				rentPer.append(trunc(rentPer_t, 3))
				averageIncome.append(format(averageIncome_t))
				restaurants.append(restaurantsT)
				ratings.append(ratingsT)
				singleHome.append(trunc(singleHome_t, 3))

			data = json.dumps({"data": {"names":places, "restaurants":restaurants, "ratings":ratings, "singleMale":sMale, "singleFemale":sFemale, "homePrice":homPrice, "singleHomes":singleHome, "rentPercent":rentPer, "averageIncome":averageIncome, "locations":locations}})
			return HttpResponse(data,mimetype='application/json')

		else:
			restaurants, ratings = yelp_table.get_restaurants(city)
			sMale, sFemale, homPrice, singleHome, rentPer, averageIncome = zillow_table.get_data(city)
			location = [str(LAT[city]), str(LONG[city])]
			data = json.dumps({"data": {"restaurants":restaurants, "ratings":ratings, "singleMale":trunc(sMale, 3), "singleFemale":trunc(sFemale,3), "homePrice":format(homPrice), "singleHomes":trunc(singleHome, 3), "rentPercent":trunc(rentPer,3), "averageIncome":format(averageIncome), "location":location}})
			return HttpResponse(data,mimetype='application/json')
			
