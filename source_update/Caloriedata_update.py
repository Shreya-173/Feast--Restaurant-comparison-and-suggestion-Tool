# update calorie information using web scraping method

import requests
import pandas as pd

def update():
    # read the page and get all text
    url ='https://raw.githubusercontent.com/PythonCharmers/PythonCharmersData/master/calories.csv'
    html_content = requests.get(url).text
    
    # Data cleaning
    calodata = pd.DataFrame()
    a = html_content.split('\n')
    food = []
    weight = []
    kCal = []
    kCal_wei = []
    del a[0]
    del a[960]

    for line in a:
        food.append(line.split('",')[0].replace('"', ''))
        wgt = float(line.split('",')[2].split(',')[0])
        kc = float(line.split('",')[2].split(',')[1])
        weight.append(wgt)
        kCal.append(kc)
        kCal_wei.append(round(kc/wgt,2))

    calodata['Food'] = food
    calodata['Weight (g)'] = weight
    calodata['kCal'] = kCal
    calodata['kCal/weight'] = kCal_wei
    
    # save the dataframe to xlsx
    calodata.to_excel('data/Calorie_Data/calorie_data.xlsx', index=False)

if __name__ == '__main__':
    update()




