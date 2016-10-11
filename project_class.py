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
        
        self.subject_ids={}

    def add_data(self, file_name):
        pass



def csv_from_excel(file_name):
    wb = xlrd.open_workbook(file_name)
    sh = wb.sheet_by_index(3)
    csv_file = open('tmp_files/temp.csv',"w", encoding='utf8',newline='')
    wr = csv.writer(csv_file,  dialect='excel')

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    csv_file.close()
    load_csv_to_db()

    
    
    
def load_csv_to_db():
    db_con = db.connect('project.db')
    csv_file = pd.read_csv("tmp_files/temp.csv")
    csv_file.to_sql("name",flavor="sqlite",con=db_con,index=False)
    
    c = db_con.cursor()
    c.execute("ALTER TABLE name ADD COLUMN group_id INTEGER DEFAULT 0")


    db_con.commit()
    
    db_con.close()