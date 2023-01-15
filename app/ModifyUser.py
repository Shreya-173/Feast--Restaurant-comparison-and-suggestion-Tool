import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
import pandas as pd


def ModifyRoot():
    modifyRoot = tk.Tk()
    modifyRoot.title('Welcome to Feast！')
    modifyRoot.geometry('400x400+300+300')
    modifyRoot['bg'] = 'lightblue'
    modifyRoot.attributes('-alpha', 1)

    # Click 'submit'
    def clickSubR():
        ioC2 = r'data/Calorie_Data/PersonalInfo.xlsx'
        data = pd.read_excel(ioC2, sheet_name=0, names=['Date', 'Sex', 'Weight', 'Height', 'Age', 'Activity level', 'CalorieRecom'])

        # data = openpyxl.load_workbook('data/Calorie_Data/PersonalInfo.xlsx')
        # sheetnames = data.get_sheet_names()
        # table = data.get_sheet_by_name(sheetnames[0])
        # table = data.active
        # nrows = table.max_row
        # ncolumns = 1

        date = str(DateNum.get())
        sex = combsex.get()
        weight = int(weightvalue.get())
        height = int(heightvalue.get())
        age = int(agevalue.get())
        actlevel = combact.get()

        if sex =='Female':
            calorieTemp = (10*weight) + (6.25*height) - (5*age) - 161
        elif sex =='Male':
            calorieTemp = (10 * weight) + (6.25 * height) - (5 * age) + 5

        if actlevel=='Sedentary':
            CalorieRecom = calorieTemp*1.2
        elif actlevel=='Lightly active':
            CalorieRecom = calorieTemp * 1.375
        elif actlevel == 'Moderately active':
            CalorieRecom = calorieTemp * 1.55
        elif actlevel == 'Active':
            CalorieRecom = calorieTemp * 1.725
        elif actlevel == 'Very active':
            CalorieRecom = calorieTemp * 1.9

        values = [date, sex, weight, height, age, actlevel, CalorieRecom]  
        # for value in values:
        #     table.cell(nrows + 1, ncolumns).value = value   
        #     ncolumns = ncolumns + 1 
        for i in range(len(data)):
            if date == data["Date"][i]:
                data.loc[i] = values
                break
            elif i == len(data)-1:
                data.loc[i+1] = values
        if len(data) == 0:
            data.loc[0] = values
        data= data.sort_values('Date')


        data.to_excel(r'data/Calorie_Data/PersonalInfo.xlsx', sheet_name="Sheet1", index = False)
        #data.save(r'data/Calorie_Data/PersonalInfo.xlsx')                   
        messagebox.showinfo('Hi', 'Successfully submitted！')
        modifyRoot.destroy()
        

    # Click 'back'
    def clickReturnR():
        modifyRoot.destroy()
        
        

    # initialize
    dateRoot = tk.Frame(modifyRoot, bg='lightblue')
    dateRoot.pack()

    sexRoot = tk.Frame(modifyRoot, bg='lightblue')
    sexRoot.pack()

    weightRoot = tk.Frame(modifyRoot, bg='lightblue')
    weightRoot.pack()

    heightRoot = tk.Frame(modifyRoot, bg='lightblue')
    heightRoot.pack()

    heightRoot = tk.Frame(modifyRoot, bg='lightblue')
    heightRoot.pack()

    ageRoot = tk.Frame(modifyRoot, bg='lightblue')
    ageRoot.pack()

    actRoot = tk.Frame(modifyRoot, bg='lightblue')
    actRoot.pack()

    btnRoot = tk.Frame(modifyRoot, bg='lightblue')
    btnRoot.pack()

    # get user input
    var_date = tk.StringVar()
    var_sex = tk.StringVar()
    var_weight = tk.StringVar()
    var_height = tk.StringVar()
    var_age = tk.StringVar()
    var_actlevel = tk.StringVar()

    # Date
    tk.Label(dateRoot, text='Date(mm-dd-yyyy)', bg='lightblue').grid(row=1, column=0, ipady=20, ipadx=0)
    DateNum = Entry(dateRoot, textvariable=var_date)
    DateNum.grid(row=1, column=1, columnspan=3)

    # sex
    tk.Label(sexRoot, text='Sex', bg='lightblue').grid(row=2, column=0, ipady=15, ipadx=47)
    combsex = Combobox(sexRoot, textvariable=var_sex, values=['Female', 'Male'], width=18)
    combsex.grid(row=2, column=1)

    # weight
    tk.Label(weightRoot, text='Weight (kg, integer)', bg='lightblue').grid(row=3, column=0, ipady=15, ipadx=2)
    weightvalue = Entry(weightRoot, textvariable=var_weight)
    weightvalue.grid(row=3, column=1, columnspan=3)

    # Height
    tk.Label(heightRoot, text='Height (cm, interger)', bg='lightblue').grid(row=4, column=0, ipady=15, ipadx=2)
    heightvalue = Entry(heightRoot, textvariable=var_height)
    heightvalue.grid(row=4, column=1, columnspan=3)

    # Age
    tk.Label(ageRoot, text='Age (interger)', bg='lightblue').grid(row=5, column=0, ipady=15, ipadx=15)
    agevalue = Entry(ageRoot, textvariable=var_age)
    agevalue.grid(row=5, column=1, columnspan=3)

    # Activity level
    tk.Label(actRoot, text='Activity level', bg='lightblue').grid(row=6, column=0, ipady=15, ipadx=22)
    combact = Combobox(actRoot, textvariable=var_actlevel, values=['Sedentary', 'Lightly active', 'Moderately active', 'Active', 'Very active'], width=18)
    combact.grid(row=6, column=1)

    # show the buttons
    Button(btnRoot, text='submit', width=6, command=clickSubR).grid(row=7, column=0)
    Button(btnRoot, text='back', width=6, command=clickReturnR).grid(row=7, column=1)

    modifyRoot.mainloop()

if __name__ == '__main__':
    ModifyRoot()