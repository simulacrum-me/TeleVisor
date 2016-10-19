# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:38:52 2016

@author: Simulacrum
"""
import pandas as pd
import xlrd
import csv
import sqlite3 as db

from subject_class import Subject

class Project_data:
    
    def __init__(self, project_path):
              
        self.name = project_path.rsplit(sep="/",maxsplit=1)[1][:-4]
        
    def add_data(self, file_name):        
        self.csv_from_excel(file_name)
        subject_name = file_name.rsplit(sep="/",maxsplit=1)[1][:-4]
        self.load_csv_to_db(subject_name)
        self.add_meta_data(subject_name)
        self.filter_for_ponemah(subject_name)
        if len(self.subjects) == 1:
            self.prepare_table_structure(subject_name)
        self.merge_to_main_db(subject_name)
    
    def merge_to_main_db(self, subject_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("INSERT INTO project_data SELECT * FROM "+subject_name)
        c.execute("DROP TABLE "+subject_name)
        db_con.commit() 
        db_con.close()
        
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
        db_con.close()
        
    def add_meta_data(self, subject_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        try:
            subject_id = max([subject.id for subject in self.subjects]) + 1
        except AttributeError:
            subject_id = 0
            self.subjects=[]

        self.subjects.append(Subject(id=subject_id,name=subject_name,group=0))
        c.execute("ALTER TABLE "+subject_name+" ADD COLUMN subject_id INTEGER DEFAULT "+str(subject_id))
        
        db_con.commit() 
        db_con.close()
        
    def prepare_table_structure(self, subject_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("CREATE TABLE project_data AS SELECT * FROM "+subject_name+" WHERE 1=2")
        db_con.commit() 
        db_con.close()
    def get_attribute_data(self, subject_id, attribute_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("select `"+attribute_name+"` from project_data where `subject_id` = "+str(subject_id))
        buffer = c.fetchall()
        db_con.commit() 
        db_con.close()
        return buffer
        
    def get_attribute_names(self):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("PRAGMA table_info(project_data)")
        buffer = c.fetchall()
        db_con.commit() 
        db_con.close()
        return [names[1] for names in buffer]
        
    def filter_for_ponemah(self, subject_name):
        db_con = db.connect(self.name+".db")
        c = db_con.cursor()
        c.execute("DELETE FROM "+subject_name+" WHERE `HR:ECG` >= 9999900414574590")
        db_con.commit() 
        db_con.close()
        
    def get_subjects_names(self):
        try:
            return [subject.name for subject in self.subjects]
        except AttributeError:
            return []