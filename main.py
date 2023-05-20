from tkinter import IntVar, ttk
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import traceback
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

            if self.file_path:
                # Code to determine dependent and independent variables
                df = self.feature_engineering(df)
                # Code for data cleaning
                df = self.check_clean(df)
                # Code to check for missing data
                df = self.check_missing_data(df)
                # Code to check if data is normal
                df = self.check_normality(df)
            
        except Exception as e:
            print(e)
    def feature_engineering(self,df):
        messagebox.showinfo("Information:","Select COLUMNS for DEPENDENT VARIABLE(y):")
        self.dep_var_label = ttk.Label(self.root,text="Select dependent/target variable:")
        self.dep_var_label.grid(row=1,column=1)
        self.dependent_var = ttk.Combobox(self.root,values=df.columns)
        self.dependent_var.grid(row=1,column=3)

        self.indep_var_label = ttk.Label(self.root,text="Select independent variable(X):")
        self.indep_var_label.grid(row=2,column=1)

        self.checkButtonVal = []
        self.CheckButton = []
        # messagebox.showinfo("info",len(df.columns))
        try:
            for i in range(0,len(df.columns)):
                self.checkButtonVal.append(IntVar())
                self.CheckButton.append(ttk.Checkbutton(self.root,text=df.columns[i],onvalue=1,offvalue=0,
                                                      variable=self.checkButtonVal[i],width=20,command=lambda:self.toggleCheck(i)))
                self.CheckButton[i].grid(row=i+2,column=3)
        except Exception as e:
            traceback.print_exc()    

    def toggleCheck(self,i):
        self.checkButtonVal[i] = not self.checkButtonVal[i]
        

    
    def check_clean(self,df):
        pass
    
    def check_missing_data(self,df):
        pass

    def check_normality(self,df):
        pass
        


EDA()
