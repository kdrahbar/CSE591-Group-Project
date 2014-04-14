import requests
import urllib2
from xml.dom.minidom import parseString
from datetime import datetime
from hashlib import sha1, md5
from random import random
from time import time
from urllib import quote
from urlparse import parse_qsl, urljoin, urlsplit
import oauth2
import mysql.connector

CITIES = ['Tempe', 'Phoenix', 'Scottsdale', 'Chandler', 'Laveen', 'Goodyear', 'Buckeye', 'Glendale', 'Peoria', 'Gilbert', 'Mesa', 'Tolleson']
DB_NAME = 'yelp_zillow'

######### YELP MANAGE API INFO ###########
consumer_key = 'GnKoz65n6F1T2OiMB-CwQw'
consumer_secret = 'O5kt8HQjj1nCdWsrIaXOaVyWUr0'
token = 'RWH5mtwnXiMfQFEc3k2ElG8_PKDQ4UNO'
token_secret = 'HCJBywpOO1oowJsOD3ElSiK8cHI'
###########################################

def get_names_ratings(json_res):
	businesses = []
	for key, value in json_res.iteritems():
		if key == 'businesses':
			businesses = value
	names = []
	ratings = []
	for business_dict in businesses:
		if 'rating' and 'id' in business_dict:
			for key, value in business_dict.iteritems():
				if 'rating' in key and(len(key) == 6):
					ratings.append(value)
				elif 'name' in key and (len(key) == 4):
					names.append(value)
	return names, ratings

def oauth_request(url):
	token = 'RWH5mtwnXiMfQFEc3k2ElG8_PKDQ4UNO'
	consumer = oauth2.Consumer(consumer_key,consumer_secret)
	oauth_request = oauth2.Request('GET', url, {})
	oauth_request.update({'oauth_nonce' : oauth2.generate_nonce(),
						 'oauth_timestamp' : oauth2.generate_timestamp(),
						 'oauth_token' : token,
						 'oauth_consumer_key' : consumer_key })	

	token = oauth2.Token(token, token_secret)
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
	return oauth_request.to_url()

URL = 'http://api.yelp.com/v2/search?term=food&location='
add_rest = ("INSERT INTO yelp (restaurant_name, city_name, rating) VALUES (%s, %s, %s)")
cnx = mysql.connector.connect(user='root', database=DB_NAME)
cursor = cnx.cursor()
for city in CITIES:
	url = URL + city
	signed_url = oauth_request(url)
	r = requests.get(signed_url)
	json_res = r.json()
	names, ratings = get_names_ratings(json_res)
	print names, ratings
	for name, rate in zip(names, ratings):
		insert_data = (name, city, rate)
		cursor.execute(add_rest, insert_data)
		cnx.commit()
cursor.close()
cnx.close()