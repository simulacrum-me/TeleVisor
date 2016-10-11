# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:38:52 2016

@author: Simulacrum
"""
import pandas as pd
import xlrd
import csv
import sqlite3 as db

class Project_data:
    
    def __init__(self, project_path):
      
        self.subject_ids=set()
        self.name = project_path.rsplit(sep="/",maxsplit=1)[1][:-4]
        
    def add_data(self, file_name):
        if len(self.subject_ids) == 0:
            self.csv_from_excel(file_name)
            subject_name = file_name.rsplit(sep="/",maxsplit=1)[1][:-4]
            self.load_csv_to_db(subject_name)



    def csv_from_excel(self,file_name):
        wb = xlrd.open_workbook(file_name)
        sh = wb.sheet_by_index(3)
        csv_file = open('tmp_files/temp.csv',"w", encoding='utf8',newline='')
        wr = csv.writer(csv_file,  dialect='excel')
    
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        csv_file.close()
        
    
    def load_csv_to_db(self, subject_name):
        db_con = db.connect(self.name+".db")
        csv_file = pd.read_csv("tmp_files/temp.csv")
        csv_file.to_sql(subject_name,flavor="sqlite",con=db_con,index=False)
        c = db_con.cursor()
        subject_id = max(self.subject_ids)+1 if len(self.subject_ids) else 0
        self.subject_ids.add(subject_id)
        print(subject_id)
        c.execute("ALTER TABLE "+subject_name+" ADD COLUMN subject_id INTEGER DEFAULT "+str(subject_id))
        db_con.commit() 
        db_con.close()
        
    def prepare_table_structure(self, table_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("CREATE TABLE project_data AS SELECT * FROM "+table_name+" WHERE 1=2")
        db_con.commit() 
        db_con.close()