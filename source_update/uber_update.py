# Credit to Alan Chin/ychin
# update restaurant list on uber using web scraping method
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import time
import random
 
# setting path
sys.path.append('../FEAST')

def update():
    #set up parameters
    global rid, items_id
    rid = 0
    items_id =0

    #set up the sources url to be retreived 
    type_dict ={"Fast Food":"https://www.ubereats.com/category/pittsburgh-pa/fast-food",
                "Chinese Food":"https://www.ubereats.com/category/pittsburgh-pa/chinese",
            "Indian Food":"https://www.ubereats.com/category/pittsburgh-pa/indian"}
    
    #set up final table to store all the restaurants
    res_res = pd.DataFrame()
    res_items = pd.DataFrame()
    
    for i in type_dict.keys():
        
        uber_restaurants = {"restaurant_id":[], 'restaurant_name':[],"restaurant_type":[],
                        'address':[],'rating':[] ,"avg_price":[],"rating_numbers":[],'comments':[],'url':[], "delivery_fee":[],"avg_dilivery_time":[]}
        uber_items = {"items_id":[], "restaurant_id":[], "items_name":[] , "items_price":[]}
        soup = fetch_page(type_dict[i])
        get_rname(soup,i,uber_restaurants) #get restaurant name
        get_delivery_info(soup,uber_restaurants)
        get_rating(soup,uber_restaurants) #get rating
        get_url(soup,uber_restaurants) #get url
        
        #use the fetched urls in uber_restaurants["url"] to dig deeper into each "restaurant page", 
        #so that we could get address and items
        
        for j in range(len(uber_restaurants["url"])):
            print("updating uber eats data...")  
            #get the bf4 object of "restaurant page"
            try:
                r_page = fetch_page(uber_restaurants["url"][j])
            except:
                uber_restaurants["address"].append("None")
                uber_restaurants["rating_numbers"].append("None")
                uber_restaurants["comments"].append("None")
                uber_restaurants["avg_price"].append("None")
                continue
            #get_menu_items
            get_items(r_page,j,uber_items,uber_restaurants)
            
            #get_rating_numbers
            get_rating_numbers(r_page,uber_restaurants)
            
            #get_comments
            get_comments(r_page,uber_restaurants)
            
            #get_restaurant adress/which include another fetch page process in the function
            get_address(r_page,uber_restaurants)
            
            # print(j,uber_restaurants["restaurant_name"][j],uber_restaurants["address"][j], 
            #       uber_restaurants["avg_dilivery_time"][j], uber_restaurants["delivery_fee"][j],
            #      uber_restaurants["rating_numbers"][j])
            
        
        restaurants = pd.DataFrame(data=uber_restaurants)
        items = pd.DataFrame(data=uber_items)

        res_res = pd.concat([res_res, restaurants])
        res_items = pd.concat([res_items, items])
        
    res_res.to_csv("data//uber_rest.csv",index=False)
    res_items.to_csv("data//uber_items.csv",index=False)


    #save the result to data//uber_rest.csv
    return None

#feel free to define other function, 
#but make sure they are call in update() since our main app only calls the update()
"""""""""""""""""""""""""""
get bf4 object from url
url (str) : the target url we like to fetch
"""""""""""""""""""""""""""
def fetch_page(url):
    #setting up sleep time to aviod frequency error
    time.sleep(random.uniform(1, 2))
    land_url = url
    land_req = Request(land_url, headers={'User-Agent' : 'Mozilla/5.0'})
    land_page = urlopen(land_req).read() 
    land_soup = BeautifulSoup(land_page, 'html.parser')
    return land_soup

"""""""""""""""""""""""""""
get restaurant name
locating method : In this case find h3, most of restaurant name on uber are in h3
Excecption: Some h3 are Q&A questions that we don't want, we could get rid of it by detecting whether "?" is in the text

Tips
(it is just about finding the pattern to locate the data you want 
and also find pattern in the data you don't want to get rid off it )
"""""""""""""""""""""""""""
def get_rname(soup,ftype,uber_restaurants):
    global rid
    r_name =soup.findAll('h3')
    for x in r_name:
        if "?" in x.text:
            break
        uber_restaurants["restaurant_id"].append(rid)
        uber_restaurants["restaurant_name"].append(x.text)
        uber_restaurants["restaurant_type"].append(ftype)
        rid+=1

"""""""""""""""""""""""""""
get restaurant rating
locating method : find div, which has text with length = 3 and have ".", since rating format is always "X.X" ex. 4.3
Excecption: Some new stores does not have numerical rating, but only shows New, we append None instead

soup (bf4object):  the fetched data from  fetch_page(url) function 
uber_restaurants (dict): the dict to store the data       
"""""""""""""""""""""""""""
def get_rating(soup,uber_restaurants):
    r_rating = soup.find_all("div")
    for x in r_rating:
        if len(x.text) ==3:
            if x.text[1] ==".":
                uber_restaurants['rating'].append(x.text)
            elif x.text == "New":
                uber_restaurants['rating'].append(None)

def get_delivery_info(soup,uber_restaurants):
    r_dt = soup.find_all("span")
    for x in r_dt:
        if len(x.text) <11:
            if x.text[-3:] =="min":
                try:
                    uber_restaurants["avg_dilivery_time"].append((int(x.text[0:2]),int(x.text[3:5])))
                except:
                    uber_restaurants["avg_dilivery_time"].append(None)
        if x.text[-12:] == "Delivery Fee":
            uber_restaurants["delivery_fee"].append(float(x.text[1:-13]))
        
    for i in range(len(uber_restaurants["avg_dilivery_time"]), len(uber_restaurants["restaurant_id"])): 
        uber_restaurants["avg_dilivery_time"].append(None)
        uber_restaurants["delivery_fee"].append(None)

"""""""""""""""""""""""""""
get restaurant url
locate method: herf
soup (bf4object):  the fetched data from  fetch_page(url) function 
uber_restaurants (dict): the dict to store the data       
"""""""""""""""""""""""""""
def get_url(soup,uber_restaurants):
    r_url = soup.select("a[href*=store]")
    for x in range(1,len(uber_restaurants["restaurant_name"])+1):
        uber_restaurants["url"].append("https://www.ubereats.com" + r_url[x]["href"])

"""""""""""""""""""""""""""
get restaurant address
locate method: text end with PA, 15xxx
land_soup (bf4object):  the fetched data from  fetch_page(url) function, in this case it is the url in uber_restaurant["url"]
uber_restaurants (dict): the dict to store the data    

"""""""""""""""""""""""""""
def get_address(land_soup,uber_restaurants): 
    
    #we could locate the html object with specific text 
    more = land_soup.find_all("a",text = "More info")    
    
    #get the url from the more object by ["href"]
    res = "https://www.ubereats.com" + more[0]["href"]
    
    #fetch the bf4 object for the url that you want to dig into futher
    ad_soup = fetch_page(res)
    
    #Then use the bf4 object to get the data
    r_ad = ad_soup.findAll("div")
    for i in range(len(r_ad)):
        if "PA 15" in r_ad[i].text[-8:-2]:
            uber_restaurants["address"].append(r_ad[i].text)
            break
        elif i == len(r_ad)-1:
            uber_restaurants["address"].append("None")

"""""""""""""""""""""""""""
get menu items
"""""""""""""""""""""""""""
def get_items(land_soup,j,uber_items,uber_restaurants):
    global items_id
    r_f_p =land_soup.findAll("div", tabindex = "0")
    count = 0
    sum_price = 0
    for x in r_f_p:
        f_p = x.find_all("span")
        f_p[0].text
        
        uber_items["items_id"].append(items_id)
        uber_items["restaurant_id"].append(uber_restaurants["restaurant_id"][j])
        uber_items["items_name"].append(f_p[0].text) 
        try:
            if f_p[1].text[0] == '$' and len(f_p[1].text)>1:
                uber_items["items_price"].append(f_p[1].text)
                count+=1
                sum_price += float(f_p[1].text[1:])
            else:
                uber_items["items_price"].append(None)
        except:
            uber_items["items_price"].append(None)
        items_id+=1
    if count != 0:
        uber_restaurants["avg_price"].append(sum_price/count)
    else:
        uber_restaurants["avg_price"].append(None)
"""""""""""""""""""""""""""
get rating_numbers
"""""""""""""""""""""""""""
def get_rating_numbers(land_soup,uber_restaurants):
    try:
        r_n =land_soup.find("img", width = "14").parent
        start= False
        res = ""
        for i in r_n.text:
            if i == "(":
                start = True
            elif start:
                if i.isnumeric():
                    res+=i
                else:
                    break
        if res =="":
            res =None
        uber_restaurants["rating_numbers"].append(res)
    except:
        uber_restaurants["rating_numbers"].append(None)
"""""""""""""""""""""""""""
get comments
"""""""""""""""""""""""""""
def get_comments(land_soup,uber_restaurants):
    try:
        r_c =land_soup.find("section", id="store-desktop-reviews")
        c_list = r_c.findAll("span")
        res = set()
        for i in range(1,len(c_list),2):
            res.add(c_list[i].text)
        uber_restaurants['comments'].append(res)
    except:
        uber_restaurants['comments'].append({})
