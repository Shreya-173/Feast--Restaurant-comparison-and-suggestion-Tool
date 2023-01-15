import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
import pandas as pd



def ModifyCalorie():
    modifyRoot = tk.Tk()
    modifyRoot.title('Add a diet record！')
    modifyRoot.geometry('600x350+300+300')
    modifyRoot['bg'] = 'lightblue'
    modifyRoot.attributes('-alpha', 1)

    # After you click Submit
    def clickSubR():
        ioC2 = r'data/Calorie_Data/Foodrecord.xlsx'
        data = pd.read_excel(ioC2, sheet_name=0, names=['Date', 'Food', 'Weight(g)', 'kCal'])
        # data = openpyxl.load_workbook(r'data/Calorie_Data/Foodrecord.xlsx')
        # sheetnames = data.get_sheet_names()
        # table = data.get_sheet_by_name(sheetnames[0])
        # table = data.active
        # nrows = table.max_row
        # ncolumns = 1

        date = str(DateNum.get())
        food = combsex.get()
        weight = int(weightvalue.get())

        count = 0
        for line in dataC1['Food']:
            count += 1
            if food == line:
                kCal = dataC1['kCal/weight'][count - 1] * weight

        values = [date, food, weight, kCal]  

        for i in range(len(data)):
            if i == len(data)-1:
                data.loc[i+1] = values
        if len(data) == 0:
            data.loc[0] = values
        data= data.sort_values('Date')
        data.to_excel(r'data/Calorie_Data/Foodrecord.xlsx', sheet_name="Sheet1", index = False)
        
                         
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

    btnRoot = tk.Frame(modifyRoot, bg='lightblue')
    btnRoot.pack()

    # get input
    var_date = tk.StringVar()
    var_food = tk.StringVar()
    var_weight = tk.StringVar()


    # Date
    tk.Label(dateRoot, text='Date(mm-dd-yyyy)', bg='lightblue').grid(row=1, column=0, ipady=30, ipadx=0)
    DateNum = Entry(dateRoot, textvariable=var_date)
    DateNum.grid(row=1, column=1, columnspan=3)

    # Food
    ioC = r'data/Calorie_Data/calorie_data.xlsx'
    dataC1 = pd.read_excel(ioC, sheet_name=0, names=['Food', 'Weight(g)', 'kCal', 'kCal/weight'])

    menu = []
    for i in dataC1['Food']:
        menu.append(i)
    calperweight = []
    for i in dataC1['kCal/weight']:
        calperweight.append(i)

    tk.Label(sexRoot, text='Food', bg='lightblue').grid(row=2, column=0, ipady=30, ipadx=39)
    combsex = Combobox(sexRoot, textvariable=var_food, values= menu, width=18)
    combsex.grid(row=2, column=1, columnspan=3)

    # weight
    tk.Label(weightRoot, text='Weight(g)', bg='lightblue').grid(row=3, column=0, ipady=30, ipadx=23)
    weightvalue = Entry(weightRoot, textvariable=var_weight)
    weightvalue.grid(row=3, column=1, columnspan=3)

    # show button
    Button(btnRoot, text='submit', width=6, command=clickSubR).grid(row=7, column=0)
    Button(btnRoot, text='back', width=6, command=clickReturnR).grid(row=7, column=1)

    modifyRoot.mainloop()

if __name__ == '__main__':
    ModifyCalorie()