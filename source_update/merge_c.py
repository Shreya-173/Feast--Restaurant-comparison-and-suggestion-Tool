# This file is where I will practice merging the data into one main dataframe
# address seems to be the most natural identifier, so I will try to merge based on that.

import pandas as pd
import numpy as np
import re
import statistics
import string

import sys
# setting path
sys.path.append("../FEAST")


def merge():
    # Google data
    dfG1 = pd.read_csv('data/google_api_update.csv', index_col=0)
    colG = dfG1.columns.values
    # colG[2] = 'address'
    # Uber_Eats data
    dfU = pd.read_csv('data/uber_rest.csv', index_col=0)
    # DoorDash data
    dfD = pd.read_csv('data/doordash_rest.csv', index_col=0, encoding="utf-8")
    # make sure all columns are visible
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # trims off the district part in address
    dfG1['address'] = [string.capwords(value.rpartition(',')[0]) for value in dfG1['address']]

    # this code trims off the address added on Uber data
    dfU = dfU[dfU['address'].notna()]
    dfU['address'] = [value[0:-10] for value in dfU['address']]
    dfU['address'] = [string.capwords(value.rpartition(',')[0]) for value in dfU['address']]
    dfU['address'] = [string.capwords(value.replace(".", "")) for value in dfU['address']]
    dfU['address'] = [string.capwords(value.replace("Road", "Rd")) for value in dfU['address']]
    dfU['address'] = [string.capwords(value.replace("Boulevard", "Blvd")) for value in dfU['address']]
    dfU['address'] = [string.capwords(value.replace("Avenue", "Ave")) for value in dfU['address']]
    dfU['address'] = [string.capwords(value.replace("Street", "St")) for value in dfU['address']]

    # format doordash restaurant address
    dfD = dfD[dfD['address'].notna()]
    dfD['address'] = [string.capwords(str(address).replace('Street', 'St')) for address in dfD['address']]
    dfD['address'] = [string.capwords(str(address).replace('Avenue', 'Ave')) for address in dfD['address']]
    dfD['address'] = [string.capwords(str(address).replace('Boulevard', 'Blvd')) for address in dfD['address']]
    dfD['address'] = [string.capwords(str(address).replace('Road', 'Rd')) for address in dfD['address']]

    # test2 = 'Taco Bell (705 Allegheny Avenue)'

    # print(dfU['restaurant_name'])

    # merge the data
    # dfM = pd.merge(dfG, dfU, on='address', how='outer')
    # pd.set_option('display.max_rows', None)
    # print(dfM[['Place Name', 'address', 'restaurant_name']])  #### REMEMBER, check that you haven't changed Place Name yet
    # this was mildly helpful, it did make some good merges, but it also had some repeats because of multiple locations.

    # Attempt to merge on address and name

    # clean unnecessary notes in google restaurants' names
    dfG1['restaurant_name'] = [string.capwords(name)if '(' not in name else string.capwords(re.split(r'\(', name)[0].strip()) for name in dfG1['restaurant_name']]
    dfG1['restaurant_name'] = [string.capwords(name) if '（' not in name else string.capwords(re.split(r'（', name)[0].strip()) for name in
                               dfG1['restaurant_name']]
    dfG1['restaurant_name'] = [string.capwords(name) if ' | ' not in name else string.capwords(re.split(r' \| ', name)[0].strip()) for name in
                               dfG1['restaurant_name']]
    dfG1['restaurant_name'] = [string.capwords(name) if ' -' and '- ' not in name else string.capwords(re.split(r'-', name)[0].strip()) for name in
                               dfG1['restaurant_name']]

    # first, more string manipulation to remove address info from uber name; change google column name
    dfU['restaurant_name'] = [string.capwords(value.split('(')[0].strip()) if '(' in value else string.capwords(value.strip()) for value in dfU['restaurant_name']]
    dfU['restaurant_name'] = [string.capwords(name) if ' -' and '- ' not in name else string.capwords(re.split(r'-', name)[0].strip()) for name in dfU['restaurant_name']]
    dfU['restaurant_name'] = [string.capwords(name) if '[' not in name else string.capwords(re.split(r'\[', name)[0].strip()) for name in
                              dfU['restaurant_name']]
    pd.set_option('display.max_rows', None)

    dfD['restaurant_name'] = [string.capwords(name) for name in dfD['restaurant_name']]
    dfD['restaurant_name'] = [name.replace('&', 'and') for name in dfD['restaurant_name']]

    # colG[0] = 'restaurant_name'
    # dfG.columns = colG
    # print("\nColumns of the google data")
    # print(dfG1.columns)

    # print("\nColumns of the uber data")
    # print(dfU.columns)

    # print("\nColumns of the doordash data")
    # print(dfD.columns)

    # second, attempt the merge using both columns for on=
    dfM = pd.merge(dfG1, dfU, on=['address', 'restaurant_name'], how='outer')
    dfM1 = pd.merge(dfM, dfD, on=['address', 'restaurant_name'], how='outer')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # print("\nMerged data information")
    # print(len(dfM1.index))
    # print(dfM1.columns)

    # print("\nMerged data information after removing duplicates on name and address")
    dfM2 = dfM1.drop_duplicates(subset=['address', 'restaurant_name'])
    # print(len(dfM2.index))
    # print(dfM2)

    # format rating / rating number and calculate avg rating
    dfM2['rating_G'] = dfM2.fillna(0)['rating_G']
    dfM2['rating_numbers_G'] = dfM2.fillna(0)['rating_numbers_G']
    dfM2['rating_numbers'] = dfM2.fillna(0)['rating_numbers']
    dfM2['rating'] = dfM2.fillna(0)['rating']
    dfM2['Rating'] = dfM2.fillna(0)['Rating']
    dfM2['ratings_numbers'] = dfM2.fillna(0)['ratings_numbers']
    dfM2['rating_numbers'] = [float(num) if num != 'None' else 0 if num is not None else 0 for num in dfM2['rating_numbers']]
    dfM2['total_rating'] = dfM2['rating_numbers_G']+dfM2['rating_numbers']+dfM2['ratings_numbers']
    dfM2['avg_rating'] = (dfM2['rating_G']*dfM2['rating_numbers_G']+dfM2['rating']*dfM2['rating_numbers']+dfM2['Rating']*dfM2['ratings_numbers'])/dfM2['total_rating']
    dfM2['avg_rating'] = dfM2['avg_rating'].round(1)
    dfM2['total_rating'] = dfM2['total_rating'].astype(int)

    # format and calculate avg delivery time
    # dfM2['avg_dilivery_time'] = dfM2.fillna(0)['avg_dilivery_time']
    dfM2['avg_dilivery_time'] = [statistics.median([int(item) for item in re.findall(r'\d+', t)]) if type(t) is str else 0 for t in dfM2['avg_dilivery_time']]
    dfM2['delivery_time'] = [int(t[:-4]) if type(t) is str else 0 for t in dfM2['delivery_time']]
    dfM2['avg_delivery_time'] = ((dfM2['delivery_time']+dfM2['avg_dilivery_time'])/2).round(0)

    dfM2 = dfM2.drop(
        ['restaurant_id_G', 'rating_G', 'rating_numbers_G', 'rating_numbers', 'rating', 'Rating', 'ratings_numbers',
         'delivery_fee_y', 'avg_dilivery_time', 'delivery_time'], axis=1)

    dfM2 = dfM2[dfM2['address'].notna()]

    # print(dfM2)
    # print()




    dfM2.to_csv('data/google_uber_doordash_merged.csv')

if __name__ == "__main__":
    merge()


