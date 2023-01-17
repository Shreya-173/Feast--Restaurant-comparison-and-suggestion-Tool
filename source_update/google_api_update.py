# import whatever you need

import sys
import pandas as pd, numpy as np
import requests
import json
import time
from urllib.request import urlopen
# setting path
sys.path.append('../the folder where your py is in')
# under your folder where your py is, set an folder name data to store and read csv from


def update():
    #write your main code here
    final_data = []
    # Parameters
    urlopen("http://ipinfo.io/json")
    data = json.load(urlopen("http://ipinfo.io/json"))

    coordinates = [data['loc']]
    keywords = ['fast food', 'chinese', 'indian', 'mexican', 'bar', 'grill', 'italian', 'thai', 'greek', 'japanese',
                'casual', 'middle eastern', 'south american']
    restaurant = 'restaurant'
    radius = '10000'
    api_key = 'AIzaSyDHNV6UuayhjQcXORXoWEcZew9qDz5BNyQ'  # insert your Places API
    count = 0
    for coordinate in coordinates:
        for keyword in keywords:
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + coordinate + '&radius=' + str(
                radius) + '&keyword=' + str(keyword) + '&key=' + str(api_key)
            while True:
                respon = requests.get(url)
                jj = json.loads(respon.text)
                results = jj['results']
                print("google api updating")
                count += 1
                for result in results:
                    try:
                        name = result['name']
                        place_id = result['place_id']
                        lat = result['geometry']['location']['lat']
                        lng = result['geometry']['location']['lng']
                        location = (lat, lng)
                        try:
                            rating = result['rating']
                        except:
                            rating = None
                        tot_ratings = result['user_ratings_total']
                        types = result['types']
                        address = result['vicinity']
                        category = keyword
                        url2 = 'https://maps.googleapis.com/maps/api/place/details/json?fields=name%2Cprice_level%2Creview' \
                            '%2Ccurbside_pickup%2Cdelivery%2Cdine_in%2Ctakeout&place_id=' + place_id + '&key=' + api_key
                        respon2 = requests.get(url2)
                        jj2 = json.loads(respon2.text)
                        results2 = jj2['result']
                        price_level = results2.get('price_level')
                        curb = results2.get('curbside_pickup')
                        delivery = results2.get('delivery')
                        dine_in = results2.get('dine_in')
                        takeout = results2.get('takeout')
                        reviews = results2.get('reviews')
                        top_5_reviews = []
                        if (is_iter(reviews)):
                            for review in reviews:
                                top_5_reviews.append(review.get('text'))
                        else:
                            top_5_reviews.append("No reviews available")
                        data = [name, place_id, address, category, location, rating, tot_ratings, price_level, curb,
                                delivery, dine_in,
                                takeout, types, top_5_reviews]
                        final_data.append(data)
                    except:
                        continue
                    # if(restaurant in types):
                    #     final_data.append(data)
                    # time.sleep(1)
                if 'next_page_token' not in jj:
                    break
                else:
                    next_page_token = jj['next_page_token']
                    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=' + str(
                        api_key) + '&pagetoken=' + str(next_page_token)
    labels = ['restaurant_name', 'restaurant_id_G', 'address', 'category', 'location', 'rating_G',
              'rating_numbers_G', 'price_level_G', 'curbside_pickup', 'delivery', 'dine_in',
              'takeout', 'types', 'top_5_reviews']
    gAPI_df = pd.DataFrame.from_records(final_data, columns=labels)
    gAPI_df = gAPI_df.drop_duplicates(subset=['restaurant_id_G'])
    # save the result to data//googele_api.csv
    gAPI_df.to_csv('data/google_api_update.csv')
    return None

#feel free to define other function, 
#but make sure they are call in update() since our main app only calls the update()

def is_iter(v):
    try:
        iter(v)
        return True
    except:
        return False
