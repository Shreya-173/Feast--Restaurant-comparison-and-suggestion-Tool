##update menu items on doordash using web scraping method
from urllib.request import Request,urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import csv



#list to store the menu restaurant results
menulist=[]

def geturl(strurl):
#get resturants menu pages using bs4
    time.sleep(random.uniform(0.5,1.5))
    land_url=strurl
    land_req = Request(land_url, headers={'User-Agent' : 'Mozilla/5.0'})
    land_page = urlopen(land_req).read() 
    land_soup = BeautifulSoup(land_page, 'html.parser')
    fout = open('land_soup.txt', 'wt',encoding='utf-8')
    fout.write(str(land_soup))
    return land_soup

def findpricelist(land_soup):
    #get price of each menu items
    pricelist=[]
    itemprice=land_soup.findAll("span", overflow="truncate", display="block",class_="styles__TextElement-sc-3qedjx-0 gIuuHU")
    for x in itemprice:
        pricelist.append(x.text)
    return pricelist

def finditemlist(land_soup):
    #get the items' names 
    namelist=[]
    itemname=land_soup.findAll("h4")
    for x in itemname:
        namelist.append(x.text)
    return namelist

def update():
    menulist.append(['d_t_id', 'd_r_id', 'Restaurant Name', 'd_t_name', 'd_t_price', 'd_t_url'])
    # with open('data/doordash_rest.csv') as csv_file:
    #     #         next(csv_file)
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    df = pd.read_csv('data/doordash_rest.csv')

    #set up avg_price columns for doordash restaurant
    df['avg_price']=[None]*len(df["url"])
    
        
    for index, row in df.iterrows():
        print("updating doordash menu items data...")
        try:
            land_soup = geturl(row["url"])
            pricelist = findpricelist(land_soup)
            sum_price = 0

            #calculate average price for doordashrestaurants
            for i in pricelist:
                sum_price+=float(i[1:])
            df['avg_price'][index]=sum_price/len(pricelist)

            itemnamelist = finditemlist(land_soup)
            item_num = 0
            for i in range(len(itemnamelist)):
                try:
                    item_num = item_num + 1
                    menulist.append([item_num, line_count, row["restaurant_name"], itemnamelist[i], pricelist[i], row["url"]])

                except:
                    item_num = item_num + 1
                    menulist.append([item_num, line_count, row["restaurant_name"], itemnamelist[i], ' ', row["url"]])
            
        except:
            df['avg_price'][index]=None
            line_count = line_count + 1
            continue
        line_count = line_count + 1

    df.to_csv('data/doordash_rest.csv',index=False, encoding="utf-8")
        

    with open('data/doordash_items.csv', mode='w',encoding='utf-8',newline='') as menu_file:
        menu_write = csv.writer(menu_file)
        for m_list in menulist:
            menu_write.writerow(m_list)
if __name__ == '__main__':
    update()
