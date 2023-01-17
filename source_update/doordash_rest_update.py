# update restaurant list on doordash using web scraping method
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import pandas as pd
from selenium.webdriver.common.keys import Keys
import re
import requests

import sys
# setting path
sys.path.append("../FEAST")
# under your folder where your py is, set an folder name data to store and read csv from


def read_past_record():
    df_restaurants = pd.read_csv("data/doordash_rest.csv", header=0, index_col="restaurant_id")
    return df_restaurants


def get_restaurant_list(restaurants, restaurant_type, url):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    chrome.get(url)
    chrome.implicitly_wait(random.uniform(180, 200))
    time.sleep(random.uniform(1, 2.5))
    chrome.fullscreen_window()
    actions = ActionChains(chrome)

    page = 1

    while page <= 5:
        print("udating doordash restaurant data ...")
        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        time.sleep(random.uniform(1, 2.5))
        #print("running " + str(page) + " page")
        restaurant_list = soup.find('div', {'class': 'sc-9403d995-0 iuHtWR'})
        for i in restaurant_list.findAll('a', {'class': 'sc-9403d995-1 faQDzE'}):
            time.sleep(random.uniform(0.5, 1.5))
            r = dict()
            # r['restaurant_id'] = len(restaurants)
            r['restaurant_type'] = restaurant_type
            r['url'] = i.get('href')
            r_info = i.find('div', {'class': 'sc-9403d995-8 bMQVtA'})
            r['restaurant_name'] = r_info.find('h2').getText()
            pitts_subtype = r_info.find('p').getText()
            pitts_subtype_list = pitts_subtype.split('•')
            r['restaurant_subtype'] = pitts_subtype_list[1].strip()
            review = r_info.find('div', {'class': 'sc-9403d995-11 eqPptL'}).find('p',
                                                                                 {'class': 'sc-9403d995-12 eURwTi'})
            if review:
                span = review.find('span').text
                r['Rating'] = float(review.text[:-len(span)])
            restaurants.append(r)

        try:
            next_page = chrome.find_element(By.XPATH, "//button[@aria-label='go to next page']")
            time.sleep(random.uniform(1, 2.5))
            if next_page:
                page += 1
                actions.move_to_element(next_page).perform()
                next_page.click()
                WebDriverWait(chrome, 20).until(
                    EC.url_changes(url))
        except:
            break
    return restaurants
    chrome.close()


def get_restaurant_info(restaurant_list):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    # options.add_argument("--headless")
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    actions = ActionChains(chrome)
    address_sent = False
    for i in restaurant_list:

        if i.get('restaurant_subtype') in ['Desserts', 'Grocery', 'Convenience', 'Other'] or 'cater' in i.get('restaurant_name').lower():
            continue
        r_url = i.get('url')
        chrome.get(r_url)
        chrome.implicitly_wait(random.uniform(150, 200))
        time.sleep(random.uniform(0.5, 3))

        soup = BeautifulSoup(chrome.page_source, 'html.parser')
        chrome.fullscreen_window()
        # Close the enter address prompt
        chrome.implicitly_wait(random.uniform(0.5, 1.5))
        """
        if address_sent is False:
            chrome.find_element(By.CSS_SELECTOR, "[aria-label='Close Enter Your Delivery Address']").click()
        """

        # Get restaurant address
        time.sleep(random.uniform(1, 1.5))
        try:
            chrome.find_element(By.CSS_SELECTOR, "[data-anchor-id='MoreInfoButton']").click()
            address = chrome.find_element(By.CSS_SELECTOR, "[data-testid='IconInfoListCell']")
            time.sleep(random.uniform(1, 1.5))
            address_text = address.text
            address_1 = address_text.split('\n')[0]
            i['address'] = address_1
            print(i['address'])
            chrome.find_element(By.XPATH,
                                "/html/body/div[1]/main/div/div[4]/div/div[2]/div/div[2]/div[3]/div/div/button").click()

        except:
            #print(i.get('Name'), "Found no more info box")
            pass

        # Get total rating numbers
        try:
            store_info = chrome.find_element(By.CSS_SELECTOR, "[data-testid='storeInfo']").text
            if store_info:
                if 'ratings' in store_info:
                    ratings = store_info.split('\n')[5]
                    rating_num = re.search(r'[0-9,]+', ratings)
                    rating_num = rating_num.group().replace(',', '')
            i['ratings_numbers'] = int(rating_num)
            #print(i['ratings_numbers'])
        except:
            #print(i.get('Name'), "Found no rating numbers")
            continue

        # Set current address
        if address_sent is False:
            try:
                address_box = chrome.find_element(By.XPATH,
                                                  "/html/body/div[1]/main/div/div[1]/div[1]/div/header/div[2]/div[3]/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div/div[2]/input")
                time.sleep(random.uniform(0.5, 1.5))
                address_box.send_keys('4800 Forbes Avenue')
                address_box.send_keys(Keys.ARROW_DOWN)
                first_option = WebDriverWait(chrome, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/main/div/div[2]/div/div/div/span[1]")))
                first_option.click()

                save_address_button = chrome.find_element(By.CSS_SELECTOR, "[data-anchor-id='AddressEditSave']")
                time.sleep(random.uniform(1, 1.5))
                actions.move_to_element(save_address_button).perform()
                save_address_button.click()

                address_sent = True
            except:
                #print(i.get('Name'), "Found no setting address box")
                continue

        # Get recent reviews
        chrome.implicitly_wait(random.uniform(10, 30))
        try:
            review_list = chrome.find_elements(By.CSS_SELECTOR, "[data-telemetry-id='storeReviewCard']")
            time.sleep(random.uniform(1, 3))
            review_dict = {}
            for r in review_list:
                # print(r.text)
                temp_list = r.text.split('\n')
                time.sleep(random.uniform(0.5, 1))
                if len(temp_list) == 4:
                    r_split = re.findall(r'[\w]+', temp_list[3])
                    # print(r_split)
                    for word in r_split:
                        review_dict[word.capitalize()] = review_dict.get(word.capitalize(), 0) + 1
            i['comments'] = review_dict
            #print(i['comments'])
        except:
            #print(i.get('Name'), "Found no review list")
            pass

        # Get delivery time
        chrome.implicitly_wait(random.uniform(0.5, 1.5))
        try:
            delivery_time = chrome.find_element(By.CSS_SELECTOR, "[data-testid='basicInfoBoxTitle']").text
            time.sleep(random.uniform(0.5, 1))
            #print(delivery_time)
            i['delivery_time'] = delivery_time
        except:
            print(i.get('Name'), "Found no delivery time")
            continue

        # Get delivery fee
        try:
            delivery_fee = chrome.find_element(By.CSS_SELECTOR, "[data-anchor-id='MenuHeaderDeliveryFee']").text
            time.sleep(random.uniform(1, 1.5))
            delivery_fee = float(delivery_fee[1:])
            i['delivery_fee'] = delivery_fee
            #print(delivery_fee)
        except:
            #print(i.get('Name'), "Found no delivery fee")
            continue
    chrome.close()
    return restaurant_list


def update():
    restaurants = []
    restaurants = get_restaurant_list(restaurants, 'American', "https://www.doordash.com/food-delivery/pittsburgh-pa-restaurants/american")
    restaurants = get_restaurant_list(restaurants, 'Indian', "https://www.doordash.com/food-delivery/pittsburgh-pa-restaurants/indian")
    restaurants = get_restaurant_list(restaurants, 'Chinese', "https://www.doordash.com/food-delivery/pittsburgh-pa-restaurants/chinese-food")
    restaurants = get_restaurant_info(restaurants)

    df_res = pd.DataFrame(data=restaurants)
    df_res.to_csv("data/doordash_rest.csv", index_label='restaurant_id')


if __name__ == "__main__":
    update()

