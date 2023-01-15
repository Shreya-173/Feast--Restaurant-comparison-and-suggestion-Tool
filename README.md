Feast
The application provides restaurant’s information nearby CMU, allowing user to compare price and rating from multiple platforms across various websites with various search and filtering options. There are three main functions in the app, one is restaurant information system. The other is the calorie calculator. Last is a function that allows user to update the data source.

1. Environments check and Packages
Windows10
Python 3.7 above
Manually download the packages list as follow, or use the requirement.txt to download them at once
Package name
version
urllib3
1.26.4
Beautifulsoup4
4.11.1
pandas
1.2.4
selenium
4.5.0
webdriver_manager
3.8.3
requests
2.25.1
numpy
1.19.5
openpyxl
3.0.3
#API KEY for googel.api had already hard code in the update files

2. Installation process
Install Python3.7 or above
Install all necessary packages list above or install them using requirement.txt
Run the “Feast/group_4_Feast_app.py”
Instructions
Video link for introduction:
⚫ main menu

After install all the necessary package, click on “group_4_Feast_app.py” to start the menu based application
At main menu you could choose 3 function or enter 4 to exit
⚫ Restaurants Selection
After choosing Restaurants selection, you would see the menu page for Restaurants selection
Choose a way to filter the restaurant information
*Search by Restaurant Name: allow user to enter a name of a restaurant and return all matches
Search by Food Type: allow user to enter food type such as Chinese and return all matches
Search by Predefined Filters: allow user to search with advance filter
All three searches would ask user to type in the number of rows they like to display
After viewing the information on the search results(ex. comparing avg.Rating, avg.price on uber)
User could Enter Restaurant ID (number at far left) to compare Uber Eats and DoorDash Menu Pricing.
OR Enter ‘r’ to return to Restaurant Menu:
⚫ Calorie Calculator Calorie Calculator is based on python bulit in GUI tkinter.
After choosing Calorie Calculator, a GUI interface for main menu of the calculator would pop up.
Click on View Personal info to view and download past personal body information
Click on Manage Personal info to enter new personal body information
Click on View Diet record to view and download past diet record
Click on Manage Record to enter new diet information
After entering the personal information and Diet for Today, It would show how much calorie you are recommend to take.
Tree structure and description
Feast

group_4_Feast_app.py //main menu to start with
│ land_soup.txt // temp file for data update
│ requirements.txt //package list
│ restaurant_interface.py //restaurant information system interface
│
├─app //other functions (only calorie calculator)
│ │ homeCalculator.py //home page for calorie calculator
│ │ ModifyCalorie.py // input user’s food consumption and calculate calories
│ │ ModifyUser.py // input user’s body index and calculate recommended calories
│ │ ViewInfoCalo.py // view past consumption
│ │ ViewInfoUser.py // view past body index
│
│
│
├─calculator_export
│ export.txt // store the past record that user downloaded in calorie calculator
│
├─data //the folder that stores all data source obtain from scraping and API
│ │ doordash_items.csv /door dash menu items data from doordash_items_update.pyd
│ │ doordash_rest.csv //door dash menu items data from doordash_items_update.py
│ │ google_api_update.csv //google data get from google_api_update.py
│ │ google_uber_doordash_merged.csv //merged data of three platform
│ │ uber_items.csv //uber menu items data from uber_update.py
│ │ uber_rest.csv //update restaurant list on uber using web scraping method
│ │
│ └─Calorie_Data
│ calorie_data.xlsx //store the calorie calculation reference table
│ Foodrecord.xlsx //store food consumption record
│ PersonalInfo.xlsx //store user body index
│
├─source_update //the folder included all the API and web scraping py
│ Caloriedata_update.py // update calorie information using web scraping method
│ doordash_items_update.py //update menu items on doordash using web scraping method
│ doordash_rest_update.py //update restaurant list on doordash using web scraping method
│ google_api_update.py //update restaurant list on google using google API
│ merge_c.py //generate a merged data of three platform
│ uber_update.py //update restaurant list on uber using web scraping method
