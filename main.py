from tkinter import ttk
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np

class EDA():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x450')
        self.label_file_select = ttk.Label(self.root,text="Select File:")
        self.label_file_select.grid(row=0,column=1)
        self.button_file_entry = ttk.Button(self.root,text="Select File",command=self.openFile)
        self.button_file_entry.grid(row=0,column=3)

        if __name__ == '__main__':
            self.root.mainloop()

    def openFile(self):
        try:
            self.file_path = filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx"),("CSV files","*.csv")])
            f = self.file_path.split('/')[-1].split('.')
            filename = f[0]
            extension = f[1]
            df = pd.read_excel(self.file_path) if extension in ['xlsx','xls'] else pd.read_csv(self.file_path)
            # messagebox.showinfo("Columns",str(df.columns))

            # Code to check if data requires cleaning
            df = self.check_clean(df)
            # Code to check for missing data
            df = self.check_missing_data(df)
            # Code to check if data is normal
            df = self.check_normality(df)
            
        except Exception as e:
            print(e)

    
    def check_clean(self,df):
        pass
    
    def check_missing_data(self,df):
        pass

    def check_normality(self,df):
        pass
        


EDA()
