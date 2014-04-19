import mysql.connector

DB_NAME = 'yelp_zillow'

class yelp_table():
    @staticmethod
    def get_restaurants(city):
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_data = ("SELECT restaurant_name, rating FROM yelp WHERE city_name=\'" + city + "\'")
        ratings, restaurants = [], []
        try:
            cursor.execute(get_data)
            for(restaurant_name, rating) in cursor:
                restaurants.append(restaurant_name)
                ratings.append(rating)
        except mysql.connector.Error as err:
            print "Error getting restaurants from yelp table"
        finally:
            cursor.close()
            cnx.close()
        return restaurants, ratings


class zillow_table():
    @staticmethod
    def get_data(city):
        cnx = mysql.connector.connect(user='root', database=DB_NAME)
        cursor = cnx.cursor()
        get_data = ("SELECT singleMale, singleFemale, homePrice, singleHomes, rentPercent, avgIncome FROM zillow WHERE cityName=\'" + city + "\'")
        sMale, sFemale, homPrice, singleHome, rentPer, averageIncome = '', '', '', '', '', ''
        try:
            cursor.execute(get_data)
            for(singleMale, singleFemale, homePrice, singleHomes, rentPercent, avgIncome) in cursor:
                sMale = singleMale
                sFemale = singleFemale
                homPrice = homePrice
                singleHome = singleHomes
                rentPer = rentPercent
                averageIncome = avgIncome
        except mysql.connector.Error as err:
            print "Error getting zillow data"
        finally:
            cursor.close()
            cnx.close()
        return sMale, sFemale, homPrice, singleHome, rentPer, averageIncome
