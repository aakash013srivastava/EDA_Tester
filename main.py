import os
from tkinter import IntVar, StringVar, ttk
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
from scipy.stats import normaltest,shapiro,boxcox
import traceback
class EDA():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x600')
        self.label_file_select = ttk.Label(self.root,text="Select File:")
        self.label_file_select.grid(row=0,column=1)
        self.button_file_entry = ttk.Button(self.root,text="Select File",command=self.openFile)
        self.button_file_entry.grid(row=0,column=3)
        self.latest_tranx = None
        if __name__ == '__main__':
            self.root.mainloop()

    def openFile(self):
        try:
            self.file_path = filedialog.askopenfilename(filetypes=[("Excel files","*.xlsx"),("CSV files","*.csv")])
            f = self.file_path.split('/')[-1].split('.')
            filename = f[0]
            extension = f[1]
            self.df = pd.read_excel(self.file_path) if extension in ['xlsx','xls'] else pd.read_csv(self.file_path)
            

            if self.file_path:
                # Code to determine dependent and independent variables
                self.select_columns()
                # Code for data cleaning
                # print(self.df.head(8))
                self.lbl_clean_data = ttk.Label(self.root,text="Enter character to remove from column values")
                self.lbl_clean_data.grid(row=len(self.df.columns)+2,column=1)
                self.strip_val = ttk.Entry(self.root)
                self.strip_val.grid(row=len(self.df.columns)+2,column=3)
                self.btn_clean = ttk.Button(self.root,text="Clean!!!",command=self.check_clean)
                self.btn_clean.grid(row=len(self.df.columns)+3,column=3)
                
                
                # Code to convert columns to consistent types
                self.btn_col_dtypes = ttk.Button(self.root,text="Convert Col Dtype",command=self.convert_col_dtypes)
                self.btn_col_dtypes.grid(row=len(self.df.columns)+4,column=3)
                # Code to check for missing data
                self.check_missing_data()
                # Code to check if data is normal
                self.btn_normality = ttk.Button(self.root,text="Check Normality",command=self.check_normality)
                self.btn_normality.grid(row=len(self.df.columns)+8,column=3)
                #  Code to export file after EDA
                self.btn_export = ttk.Button(self.root,text="Export",command=self.export_dataset)
                self.btn_export.grid(row=len(self.df.columns)+10,column=3)
                
            
        except Exception as e:
            print(e)

    def select_columns(self):
        # messagebox.showinfo("Information:","Select COLUMNS for DEPENDENT VARIABLE(y):")
        self.dep_var_label = ttk.Label(self.root,text="Select dependent/target variable:")
        self.dep_var_label.grid(row=1,column=1)
        self.cols_list = [col for col in self.df.columns]
        self.dependent_var = ttk.Combobox(self.root,values=self.cols_list)
        self.dependent_var.grid(row=1,column=3)

        self.indep_var_label = ttk.Label(self.root,text="Select independent variable(X):")
        self.indep_var_label.grid(row=2,column=1)

        self.checkButtonVal = []
        self.CheckButton = []
        self.lbl_dtypes = []
    
        
        try:
            for i in range(0,len(self.df.columns)):
                self.checkButtonVal.append(IntVar())
                self.CheckButton.append(ttk.Checkbutton(self.root,text=self.df.columns[i],onvalue=1,offvalue=0,
                                                      variable=self.checkButtonVal[i],width=20,command=lambda:self.toggleCheck(i)))
                self.lbl_dtypes.append(ttk.Label(self.root,text=self.df.dtypes.astype(str)[i]))
                self.CheckButton[i].grid(row=i+2,column=3)
                self.lbl_dtypes[i].grid(row=i+2,column=4)
        except Exception as e:
            traceback.print_exc() 

        
    def toggleCheck(self,i):
        self.checkButtonVal[i] = not self.checkButtonVal[i]


    def check_clean(self):                
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].apply(lambda x:str(x).strip(self.strip_val.get()))

        

    def convert_col_dtypes(self):
        self.lbl_convert_dropdown = ttk.Label(self.root,text="Convert Dtype")
        self.lbl_convert_dropdown.grid(row=len(self.df.columns)+5,column=1)
        self.cols = [x for x in self.df.columns]
        self.convert_dropdown = ttk.Combobox(self.root,values = self.cols)
        self.convert_dropdown.grid(row=len(self.df.columns)+5,column=3)

        
        self.lbl_convert_dtype = ttk.Label(self.root,text="To Dtype:")
        self.lbl_convert_dtype.grid(row=len(self.df.columns)+6,column=1)
        
        self.convert_dtype_dropdown = ttk.Combobox(self.root,values = ['float64','int64','object'])
        self.convert_dtype_dropdown.grid(row=len(self.df.columns)+6,column=3)
        self.convert_dtype_btn = ttk.Button(self.root,text="Convert!",command=lambda:self.converter(self.convert_dtype_dropdown))
        self.convert_dtype_btn.grid(row=len(self.df.columns)+7,column=3)

    
    def converter(self,datatype):
        if datatype != 'object':
            self.df[self.convert_dropdown.get()] = pd.to_numeric(self.df[self.convert_dropdown.get()])
            messagebox.showinfo("Dtype:",str(self.df[self.convert_dropdown.get()].dtype))
        

    def check_missing_data(self):
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                
                self.df[col] = self.df[col].fillna('0')
            elif self.df[col].dtype in ['float64','int64']:
                
                self.df[col] = self.df[col].fillna(np.mean(self.df[col]))
            else:
                continue
 

    def check_normality(self):

        self.lbl_p = StringVar()
        stat,p = normaltest(self.df[[self.dependent_var.get()]])
        messagebox.showinfo("Untranformed P value:",str(p))
        self.lbl_p_value = ttk.Label(self.root,text="P value after normal test is:"+str(p),textvariable=self.lbl_p)
        self.lbl_p_value.grid(row=len(self.df.columns)+11,column=3)
        
        if p < 0.05:
            self.btn_log = ttk.Button(self.root,text="Apply Log Tranx",command=self.logTranx)
            self.btn_log.grid(row=len(self.df.columns)+9,column=1)

            self.btn_sqrt = ttk.Button(self.root,text="Apply Sqrt Tranx",command=self.sqrtTranx)
            self.btn_sqrt.grid(row=len(self.df.columns)+9,column=2)

            self.btn_boxcox = ttk.Button(self.root,text="Apply Boxcox Tranx",command=self.boxcoxTranx)
            self.btn_boxcox.grid(row=len(self.df.columns)+9,column=3)


    def logTranx(self):
        self.df[self.dependent_var.get()+'_log'] = np.log(self.df[self.dependent_var.get()])
        self.lbl_p.set(normaltest(self.df[[self.dependent_var.get()+'_log']])[1])
        self.latest_tranx = 'log'

    def sqrtTranx(self):
        self.df[self.dependent_var.get()+'_sqrt'] = np.sqrt(self.df[self.dependent_var.get()])
        self.lbl_p.set(normaltest(self.df[[self.dependent_var.get()+'_sqrt']])[1])
        self.latest_tranx = 'sqrt'

    def boxcoxTranx(self):
        k2,b = boxcox(self.df[self.dependent_var.get()])
        self.lbl_p.set(normaltest(self.df[[self.dependent_var.get()]])[1])
        self.latest_tranx = 'boxcox'


    def export_dataset(self):
        self.df.to_csv("exported.csv")

        messagebox.showinfo("Result:","Check File in working directory")

EDA()
