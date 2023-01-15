'''

'''

from tkinter import *
from tkinter import messagebox
import pandas as pd
from datetime import datetime

def ViewInfoDiettoday():
    viewInfoRoot = Tk()
    viewInfoRoot.title('Calorie Info Records')
    viewInfoRoot.geometry('600x350+300+300')
    viewInfoRoot['bg'] = 'lightblue'
    viewInfoRoot.attributes('-alpha', 0.9)

    # Click back
    def clickReturnR():
        viewInfoRoot.destroy()

    # click export
    def clickExportR():
        value = 1
        with open(r'calculator_export/export.txt', 'a') as file:
            ntime = datetime.utcnow()
            stime = ntime.strftime("%Y-%m-%d %H:%M:%S")
            file.write(str(readR()))
            file.write('\n')
            file.write(str(ntime))
            file.write('\n')
        messagebox.showinfo('Hi', 'Successfully download！')

    # initialize
    showInfoRoot = Frame(viewInfoRoot)
    showInfoRoot.pack()
    btnRoot = Frame(viewInfoRoot)
    btnRoot.pack()

    # show info
    textR = Text(showInfoRoot)
    textR.grid(row=0)
    textR.insert(END, readR())

    # show button
    Button(btnRoot, text='back', width=10, height=1, relief=GROOVE, command=clickReturnR).grid(row=1, column=0)
    Button(btnRoot, text='download', width=10, height=1, relief=GROOVE, command=clickExportR).grid(row=1, column=1)

    viewInfoRoot.mainloop()

# read data file
def readR():
    ioR = r'data/Calorie_Data/Foodrecord.xlsx'
    dataR = pd.read_excel(ioR, sheet_name=0, names=['Date','Food', 'Weight(g)', 'kCal'])
    return dataR

if __name__ == '__main__':
    ViewInfoDiettoday()