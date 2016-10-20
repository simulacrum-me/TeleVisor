# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:38:52 2016

@author: Simulacrum
"""
import pandas as pd
import xlrd
import csv

import time

from subject_class import Subject

class Project_data:
    
    def __init__(self, project_path):
              
        self.name = project_path.rsplit(sep="/",maxsplit=1)[1][:-4]
        
    def add_data(self, file_name):        
        self.csv_from_excel(file_name)
        subject_name = file_name.rsplit(sep="/",maxsplit=1)[1][:-4]
        
        
        csv_file = pd.read_csv("tmp_files/temp.csv")
        
        try:
            subject_id = max([subject.id for subject in self.subjects]) + 1
        except AttributeError:
            subject_id = 0
            self.subjects=[]

        self.subjects.append(Subject(id=subject_id,name=subject_name,group=0))
        csv_file.loc[:,'_subject_id'] = pd.Series([subject_id]*len(csv_file.index), index=csv_file.index)
        if len(self.subjects) == 1:
            self.project_df = csv_file.drop(csv_file.index)
        
        csv_file = csv_file[csv_file['HR:ECG']!=9999900414574592.0]
        self.project_df = pd.concat([self.project_df, csv_file], ignore_index=True)

        
    def csv_from_excel(self,file_name):
        wb = xlrd.open_workbook(file_name)
        sh = wb.sheet_by_index(3)
        csv_file = open('tmp_files/temp.csv',"w", encoding='utf8',newline='')
        wr = csv.writer(csv_file,  dialect='excel')
    
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        csv_file.close()
        
    
    def get_attribute_data(self, subject_id, attribute_name):
        
        return self.project_df[attribute_name][self.project_df['_subject_id'] == subject_id].tolist()

        
    def get_attribute_names(self):
        
        return list(self.project_df.columns.values)
        

    def get_subjects_names(self):
        try:
            return [subject.name for subject in self.subjects]
        except AttributeError:
            return []