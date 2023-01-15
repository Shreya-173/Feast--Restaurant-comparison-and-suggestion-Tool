'''
Home page of the calorie calculator
Credit to Ruifang Hu/ruifangh
'''

import tkinter as tk
from tkinter import *
import time
import openpyxl
import pandas as pd


from app.ModifyCalorie import ModifyCalorie
from app.ViewInfoCalo import ViewInfoDiettoday
from app.ViewInfoUser import ViewInfoUser
from app.ModifyUser import ModifyRoot

'''
Generate a window
'''
def HomeCal():
    homeRoot = tk.Tk()
    homeRoot.title('Calorie Calculator')
    homeRoot.geometry('600x300+300+300')
    homeRoot['bg'] = 'lightblue'
    homeRoot.attributes('-alpha', 1)

    def readS():
        ioS = r'data/Calorie_Data/PersonalInfo.xlsx'
        data = openpyxl.load_workbook(ioS)                          # read the Excel table
        table = data.get_sheet_by_name('Sheet1')                    # find the page
        nrows = table.rows                                          # get the number of lines
        for row in nrows:
            line = [col.value for col in row]                       # get the value
        
        ioC2 = r'data/Calorie_Data/Foodrecord.xlsx'
        dataC2 = pd.read_excel(ioC2, sheet_name=0, names=['Date', 'Food', 'Weight(g)', 'kCal'])

        count2 = 0
        totalcal = 0
        for line in dataC2['Date']:
            date = str(line)
            count2 += 1
            if date == time.strftime("%m-%d-%Y"):
                totalcal += dataC2['kCal'][count2 - 1]
        
        count3 = 0
        CalRecom = 0
        ioC3 = r'data/Calorie_Data/PersonalInfo.xlsx'
        dataC3 = pd.read_excel(ioC3, sheet_name=0,
                               names=['Date', 'Sex', 'Weight', 'Height', 'Age', 'Activity level', 'CalorieRecom'])
        for i in range(len(dataC3['Date'])):
            date = str(dataC3['Date'][i])
            count3 += 1
            if date == time.strftime("%m-%d-%Y"):
                CalRecom = dataC3['CalorieRecom'][count3 - 1]
            
        

        showS1.configure(text=round(CalRecom, 2))  # recommend calorie
        showS2.configure(text=round(totalcal, 2))  # actual calorie
        showS3.configure(text=round(CalRecom - totalcal, 2))  # you can still intake

    # get the time
    def getTime():
        timeStr = time.strftime("%m-%d-%Y")
        Rtime.configure(text=timeStr)

    # After you click “view personal info”
    def clickBtnr1():
        ViewInfoUser()

    # After you click“manage personal info”
    def clickBtnr2():
        homeRoot.destroy()
        ModifyRoot()
        HomeCal()

    # After you click “viewinfodiettoday”
    def clickBtnr3():
        ViewInfoDiettoday()

    # After you click “manage diettoday”
    def clickBtnr4():
        homeRoot.destroy()
        ModifyCalorie()
        HomeCal()

    # After you click "back"
    def clickBtnr5():
        homeRoot.destroy()

    # show the info
    tk.Label(homeRoot, text='Recommend calorie(kcal)', bg='lightblue', width=20).grid(row=2, column=2, ipady=7)
    showS1 = tk.Label(homeRoot, text='', relief=GROOVE, width=10)
    showS1.grid(row=2, column=3, ipady=7)

    tk.Label(homeRoot, text='Calorie(kcal) taken today', bg='lightblue', width=20).grid(row=3, column=2, ipady=7)
    showS2 = tk.Label(homeRoot, text='', relief=GROOVE, width=10)
    showS2.grid(row=3, column=3, ipady=7)

    tk.Label(homeRoot, text='You can still intake', bg='lightblue', width=20).grid(row=4, column=2, ipady=7)
    showS3 = tk.Label(homeRoot, text='', relief=GROOVE, width=10)
    showS3.grid(row=4, column=3, ipady=7)

    readS()

    # show the time
    Rtime = tk.Label(homeRoot, text='', bg='lightblue')
    Rtime.grid(row=1, column=1)
    try:
        getTime()
    except:
        print()

    # show the welcome info
    Rwel = tk.Label(homeRoot, text='Your daily summary for Today', bg='lightblue')
    Rwel.grid(row=1, column=2)

    # show the button
    tk.Button(homeRoot, text='View Personal info', width=20, height=1, command=clickBtnr1, relief=GROOVE).grid(row=2, column=1, ipady=10, padx=20)
    tk.Button(homeRoot, text='Manage Personal info', width=20, height=1, command=clickBtnr2, relief=GROOVE).grid(row=3, column=1, ipady=10, padx=20)
    tk.Button(homeRoot, text='View Diet record', width=20, height=1, command=clickBtnr3, relief=GROOVE).grid(row=4, column=1, ipady=10, padx=20)
    tk.Button(homeRoot, text='Manage Diet record', width=20, height=1, command=clickBtnr4, relief=GROOVE).grid(row=5, column=1, ipady=10, padx=20)
    tk.Button(homeRoot, text='back', width=20, height=1, command=clickBtnr5, relief=GROOVE).grid(row=6, column=1, ipady=10, padx=20)

    homeRoot.mainloop()

if __name__ == '__main__':
    HomeCal()
