# Credit to Alan Chin/ychin 
# This file is the main menu for for the app
import sys
import pandas as pd
 
# # setting path

from source_update import doordash_rest_update, google_api_update, doordash_items_update ,merge_c, uber_update, Caloriedata_update
from app import homeCalculator as hc
import restaurant_interface as ri

#main menu for for the app
def main():
    print('===================================================='*2)
    print("Welcome to Feast: Pittsburgh's Restaurant Comparison App for Students\n")
    
    print(
    "Please select a service:\n\n" +
    "1) Restaurant Selection\n" +
    "2) Calorie Calculator\n" +
    "3) Update the Database (Warning it would take more than 2 hours)\n" +
    "4) Exit\n")
    
    select = input('Select from List(enter a number):  ')
    
    if select == '1':
        print('===================================================='*2)
        ri.restaurant_menu()
        main()
    elif select == '2':
        hc.HomeCal()
        main()
    elif select == '3':
        print('===================================================='*2)
        update_data()
        main()
    elif select == '4':
        print("Thanks for using Feast! See you!")
    else:
        print("Invalid entry, Please try again")
        print('===================================================='*2)
        main()

   

def update_data():
    print("start updating, it normally take more than 2 hours.")
    google_api_update.update()
    print("google data updated")
    uber_update.update()
    print("uber data updated")
    doordash_rest_update.update()
    doordash_items_update.update()
    print("doordash data updated")
    print("merging the data")
    merge_c.merge()
    print("merging completed")
    Caloriedata_update.update()
    print("calorie data updated")
    print("Update completed")

    
    return None

if __name__ == "__main__":
    main()


    


    
    

