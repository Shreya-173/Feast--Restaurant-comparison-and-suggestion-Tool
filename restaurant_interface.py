# Ryan King
# AndrewID: rdking
# This file runs the user interface for working with the restaurant information
# If the data import executes then all that is required is to run the restaurant_menu() method


import pandas as pd
import numpy as np

pd.options.display.max_colwidth = 22

# Column Name List
col_list = ['Restaurant Name', 'Address', 'Google Category', 'location', 'Google Price Level', 'Curbside Pickup',
            'Delivery', 'Dine In', 'Takeout', 'types', 'top_5_reviews',
            'restaurant_type_x', 'UberEats Avg. Price', 'comments_x', 'UberEats URL', 'delivery_fee_x',
            'restaurant_type_y', 'DoorDash URL', 'restaurant_subtype', 'comments_y',
             'DoorDash Avg. Price', 'total_rating', 'Avg. Rating','Avg. Delivery Time']

disp_col_list = ['Restaurant Name', 'Address', 'Google Category', 'Google Price Level', 'Avg. Rating',
                 'UberEats Avg. Price', 'DoorDash Avg. Price', 'UberEats URL', 'DoorDash URL']

adv_col_list = ['Restaurant Name', 'top_5_reviews', 'comments_x', 'comments_y', 'UberEats URL', 'DoorDash URL']

# I am going to read in our static dataframe for ease of use
df = pd.read_csv('data/google_uber_doordash_merged.csv', header=0, names=col_list)
df['types'].replace(np.NAN, "", inplace=True)
df['Google Category'].replace(np.NAN, "", inplace=True)

# Read in the DoorDash Menu Item Files as well
dd_col_list = ['d_t_id', 'd_r_id', 'Restaurant Name',"d_t_name", 'd_t_price',"d_t_url"]
df_DD = pd.read_csv('data/doordash_items.csv', header=None, names=dd_col_list)
df_DD.rename(mapper={'d_t_name': 'Item Name', 'd_t_price': 'Door Dash Price'}, axis=1, inplace=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)


# Read in Uber Items and Uber restaurant in order to add restaurant name to the menu items file
df_UBI = pd.read_csv('data/uber_items.csv')
df_UBI.rename(mapper={'items_name': 'Item Name', 'items_price': 'Uber Eats Price'}, axis=1, inplace=True)
df_UBR = pd.read_csv('data/uber_rest.csv')
df_UBM = pd.merge(df_UBI, df_UBR, how='outer', on='restaurant_id')






# ------------Basic Dataframe Check----------------
# print(df['types'].head(10))
# print(df.columns)
# print(df.describe())
# print(df.dtypes)
# print(df.head(10))

# ---------------Null Value Check------------------
# print(df['Google Price Level'].isna().sum())
# print(df['Curbside Pickup'].isna().sum())
# print(df['Delivery'].isna().sum())
# print(df['Dine In'].isna().sum())
# print(df['Takeout'].isna().sum())


#                       The Functions for the Predefined Filter option

# date
# dine-in option and price level above 2
def take_a_date_filter(n: int):
    resultlist = []
    for i, r in df.iterrows():
        if (r['Dine In'] == True) and (r['Google Price Level'] > 2):
            resultlist.append(i)
        else:
            continue
    if n > len(resultlist):
        print("Number of restaurants desired exceeds number available. Maximum listings are provided")
        return resultlist
    else:
        return resultlist[:n]


#This function sorts df by rating and displays the highest rated based on average rating from the three sources
def high_rating_filter(n: int):
    resultslist = []
    sorted_df = df.sort_values(by='Avg. Rating', ascending=False)
    if (n > len(sorted_df)):
        print("Number of restaurants desired exceeds number available. Maximum listings are provided")
        for i, r in sorted_df.iterrows():
            resultslist.append(i)
    else:
        for i, r in sorted_df.head(n).iterrows():
            resultslist.append(i)
    return resultslist



#This filter returns the restaurants that have received the most rating this is a function of popularity
def frequently_rated_filter(n: int):
    resultslist = []
    sorted_df = df.sort_values(by='total_rating', ascending=False)
    if (n > len(sorted_df)):
        print("Number of restaurants desired exceeds number available. Maximum listings are provided")
        for i, r in sorted_df.iterrows():
            resultslist.append(i)
    else:
        for i, r in sorted_df.head(n).iterrows():
            resultslist.append(i)
    return resultslist



#This filter returns results based on price level.
def price_level_filter(n: int, amount: int):
    resultslist = []
    for i, r in df.iterrows():
        if r['Google Price Level'] == n:
            resultslist.append(i)
        else:
            continue
    if len(resultslist) > amount:
        return resultslist[0:amount]
    elif len(resultslist) > 0 and len(resultslist) < amount:
        return resultslist
    else:
        print("No results found.")
        return resultslist


#                                The functions for searching

#This function searches by category using the Category and Type information from the data sources
def search_by_category(searchterm: str, amount: int):
    print(f"Search Results for '{searchterm}'")
    resultlist = []
    for i, r in df.iterrows():
        checklist = [str(r['Google Category']).lower(), str(r['restaurant_type_x']).lower(), str(r['restaurant_type_y']).lower(),
                     str(r['restaurant_subtype']).lower()]
        if searchterm.lower() in checklist:
            resultlist.append(i)
        else:
            continue
    if len(resultlist) >= amount:
        return resultlist[0:amount]
    elif 0 < len(resultlist) < amount:
        
        return resultlist
    else:
        return resultlist



#This function searches by name, using .lower() to avoid case sensitivity issues.
def search_by_name(choice: str, amount: int):
    print(f"Search Results for '{choice}'")
    resultlist = []
    for i, r in df.iterrows():
        if choice.lower() in r['Restaurant Name'].lower():
            resultlist.append(i)
        else:
            continue
    if len(resultlist) >= amount:
        return resultlist[0:(amount-1)]
    elif 0 < len(resultlist) < amount:
        return resultlist
    else:
        return resultlist
        restaurant_menu()


#                                These are functions about display results

#This functions finds menu item information from doordash and uber eats, combines and displays it
def show_menu_items_p(n: int):
    print('===================================================='*2)
    indexlistDD = []
    indexlistU = []
    name = df['Restaurant Name'].iloc[n]
    for i, r in df_DD.iterrows():
        if name.lower() in r['Restaurant Name'].lower():
            indexlistDD.append(i)
        else:
            continue
    df_DD1 = df_DD.iloc[indexlistDD]
    for i, r in df_UBM.iterrows():
        if name.lower() in r['restaurant_name'].lower():
            indexlistU.append(i)
        else:
            continue
    df_U1 = df_UBM.iloc[indexlistU]
    df_MI = pd.merge(df_DD1, df_U1, how='outer', on='Item Name')
    df_MI = df_MI.drop_duplicates(subset=['Item Name','Door Dash Price', 'Uber Eats Price'])
    if len(df_MI.index) > 0 :
        print(df_MI[['Item Name', 'Door Dash Price', 'Uber Eats Price']])
    else:
        print('Menu Item information not available for this restaurant.')
    return_options_p()


def show_menu_items_other(n: int):
    print('===================================================='*2)
    indexlistDD = []
    indexlistU = []
    name = df['Restaurant Name'].iloc[n]
    for i, r in df_DD.iterrows():
        if name.lower() in r['Restaurant Name'].lower():
            indexlistDD.append(i)
        else:
            continue
    df_DD1 = df_DD.iloc[indexlistDD]
    for i, r in df_UBM.iterrows():
        if name.lower() in r['restaurant_name'].lower():
            indexlistU.append(i)
        else:
            continue
    df_U1 = df_UBM.iloc[indexlistU]
    df_MI = pd.merge(df_DD1, df_U1, how='outer', on='Item Name')
    df_MI = df_MI.drop_duplicates(subset=['Item Name','Door Dash Price', 'Uber Eats Price'])
    if len(df_MI.index) > 0:
        print(df_MI[['Item Name', 'Door Dash Price', 'Uber Eats Price']])
    else:
        print('Menu Item information not available for this restaurant.')
    return_options_other()


def display(selectionList: list):
    print('===================================================='*2)
    if len(selectionList) > 0:
        print(df[disp_col_list].loc[selectionList])
    else:
        print("No results to display")




def selection_options_p():
    stch = input(
        "\nEnter Restaurant ID (number at far left) to compare Uber Eats and DoorDash Menu Pricing."
        "\nOR Enter 'r' to return to Restaurant Menu Page, 'p' to return to filters: ")
    if stch.lower() == 'r':
        stch = ''
        print('===================================================='*2)
        restaurant_menu()
    elif stch.lower() == 'p':
        stch = ''
        pre_filters()
    elif stch not in ['r', 'p']:
        try:
            stch = int(stch)
            stchlist = [stch]
            show_menu_items_p(stchlist[0])
        except ValueError:
            print("Invalid Entry, must be number.")
            selection_options_p()
    else:
        print('Invalid Input')
        selection_options_p()


def selection_options_other(resid):
    stch = input(
        "\nEnter Restaurant ID (number at far left) to compare Uber Eats and DoorDash Menu Pricing. "
        "\nOR Enter 'r' to return to Restaurant Menu: ")
    if stch.lower() == 'r':
        stch = ''
        print('===================================================='*2)
        restaurant_menu()
    elif stch not in ['r']:
        try:
            stch = int(stch)
            if stch in resid:
                stchlist = [stch]
                show_menu_items_other(stchlist[0])
            else:
                print("Invalid Entry, searh ID must be in the above table")
                selection_options_other(resid)
        except ValueError:
            print("Invalid Entry, must be number.")
            selection_options_other(resid)
    else:
        print('Invalid Input')
        selection_options_other(resid)


def return_options_p():
    stch = input("Enter 'p' to return to the Predefined Filter Menu. \nOR Enter 'r' to return to the Main Menu: ")
    if stch.lower() == 'p':
        stch = ''
        pre_filters()
    elif stch.lower() == 'r':
        stch = ''
        print('===================================================='*2)
        restaurant_menu()
    else:
        print("Invalid Input")
        return_options_p()

def return_options_other():
    stch = input("Enter 'r' to return to Restaurant Menu Page: ")
    if stch.lower() in ['r']:
        print('===================================================='*2)
        restaurant_menu()
    else:
        print("Incorrect Entry, rerouting to Main Menu.")
        print('===================================================='*2)
        restaurant_menu()


def pre_filters():
    print('===================================================='*2)
    print("Predefined Filters\n")
    print("1) Highest Rated")
    print("2) Places to Take a Date")
    print("3) Choose Price Level")
    print("4) Frequently Reviewed")
    print("5) Return to Restaurant Menu\n")
    choice = input("Select a Filter: ")
    choice = int(choice)
    if choice == 1:
        num = input("Choose the desired number of restaurants to be displayed: ")
        try:
            num = int(num)
            res = high_rating_filter(num)
            if len(res) > 0:
                display(res)
                selection_options_p()
            else:
                print("No restaurants found. Please try again")
                pre_filters()
        except ValueError:
            print("\nInvalid entry, please enter response in digits.")
            pre_filters()
    elif choice == 2:
        num = input("Choose the desired number of restaurants to be displayed: ")
        try:
            num = int(num)
            res = take_a_date_filter(num)
            if len(res) > 0:
                display(res)
                selection_options_p()
            else:
                print("No restaurants found. Please try again")
                pre_filters()
        except ValueError:
            print("\nInvalid entry, please enter response in digits.")
            pre_filters()
    elif choice == 3:
        lev = input("Enter Price Level (1-5): ")
        try:
            lev = int(lev)
            if lev < 1 or lev > 5:
                print("Invalid Price Level.")
                pre_filters()
            else:
                num = input("Choose the desired number of restaurants to be displayed: ")
                try:
                    num = int(num)
                    res = price_level_filter(lev, num)
                    if len(res) > 0:
                        display(res)
                        selection_options_p()
                    else:
                        print("No restaurants found. Please try again")
                        pre_filters()
                except ValueError:
                    print("\nInvalid entry, please enter response in digits.")
                    pre_filters()
        except ValueError:
            print("\nInvalid entry, please enter response in digits.")
            pre_filters()
    elif choice == 4:
        num = input("Choose the desired number of restaurants to be displayed: ")
        try:
            num = int(num)
            res = frequently_rated_filter(num)
            if len(res) > 0:
                display(res)
                selection_options_p()
            else:
                print("No restaurants found. Please try again")
                pre_filters()
        except ValueError:
            print("\nInvalid entry, please enter response in digits.")
            pre_filters()
    elif choice == 5:
        print('===================================================='*2)
        restaurant_menu()
    else:
        print("Invalid Entry. Try Again.")
        pre_filters()


def restaurant_menu():
    print("Feast Restaurant Menu Page\n")
    print('1)  Search by Restaurant Name')
    print('2)  Search by Food Type')
    print('3)  Search by Predefined Filters')
    print('4)  Back to top menu\n')
    ch = input('Select from List:  ')
    

    if ch == "1":
        try:
            s = input("Enter Restaurant Name: ")
            a = input("Choose the maximum number of restaurants to be displayed: ")
            a = int(a)
            res = search_by_name(s, a)
            if len(res) > 0:
                display(res)
                selection_options_other( res)
            else:
                print("No restaurants found. Check spelling and try again.")
                print('===================================================='*2)
                restaurant_menu()
        except ValueError:
            print("\nInvalid entry, please enter number of restaurants in digits.")
            print('===================================================='*2)
            restaurant_menu()
    elif ch == "2":
        try:
            s = input("Enter Food Type (ex. chinese, american, indian, italian): ")
            a = input("Choose the maximum number of restaurants to be displayed: ")
            a = int(a)
            res = search_by_category(s, a)
            
            if len(res) > 0:
                display(res)
                selection_options_other(res)
            else:
                print("No restaurants found. Check spelling and try again.")
                print('===================================================='*2)
                restaurant_menu()
        except ValueError:
            print("\nInvalid entry, please enter number of restaurants in digits.")
            print('===================================================='*2)
            restaurant_menu()
    elif ch == "3":
        pre_filters()
    elif ch == "4":
        print()
    else:
        print('\nInvalid Selection. Please try again')
        print('===================================================='*2)
        restaurant_menu()


resChosenList = []
if __name__ == "__main__": 
    restaurant_menu()

# testList = ['', 'nan', 'American', 'Delis']
# term = 'American'
# if term in testList:
#     print('Term was found')
# else:
#     print('Term was not found')


