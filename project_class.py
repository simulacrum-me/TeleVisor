# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 12:38:52 2016

@author: Simulacrum
"""
import pandas as pd
import numpy as np
import xlrd
import csv

import time
import calendar



class Project_data:
    
    def __init__(self, project_path):
              
        self.name = project_path.rsplit(sep="/",maxsplit=1)[1][:-4]
        
    def add_data(self, file_name):        
        self.csv_from_excel(file_name)
        subject_name = file_name.rsplit(sep="/",maxsplit=1)[1][:-4]
        
        
        csv_file = pd.read_csv("tmp_files/temp.csv")
        
        try:
            subject_id = max(self.subjects_df['id']) + 1
        except AttributeError:
            subject_id = 0
            self.subjects_df = pd.DataFrame(columns=["name","id","group"])

        
        self.subjects_df = self.subjects_df.append({'name': subject_name, 'id': subject_id, 'group': 0}, ignore_index=True)
       
        #self.subjects.append(Subject(id=subject_id,name=subject_name,group=0))
        csv_file.loc[:,'_subject_id'] = pd.Series([subject_id]*len(csv_file.index), index=csv_file.index)
        csv_file.loc[:,'_group_id'] = pd.Series([0]*len(csv_file.index), index=csv_file.index)
        csv_file['_time']=csv_file['RealTime'].apply(lambda x: calendar.timegm(time.strptime(x[:-28],"%Y/%m/%d %H:%M:%S")))
        
        if len(self.subjects_df.index) == 1:
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

    
        
    def get_averaged_attribute_data(self, subject_id, attribute_name):
        xdata = []
        ydata = []
        averaging_period = 60*60*12 
        
        min_time = min(self.get_attribute_data(subject_id, '_time'))
        max_time = max(self.get_attribute_data(subject_id, '_time'))
        seconds_since_day_began = min_time % (60*60*24)
        seconds_before_day_began = min_time - seconds_since_day_began
        num_tperiods_to_data = seconds_since_day_began // averaging_period
        
        start_time = seconds_before_day_began + num_tperiods_to_data * averaging_period
        n_intervals = (max_time - start_time) // averaging_period + 1
        
        for interval in range(n_intervals):
            y = self.project_df[attribute_name][(self.project_df['_subject_id'] == subject_id) & (self.project_df['_time']>= (start_time+interval*averaging_period)) &  (self.project_df['_time']<= (start_time+(interval+1)*averaging_period))].tolist()
            y = np.average(y)   
            ydata.append(y)
            xdata.append(start_time+interval*averaging_period + 0.5 * averaging_period)                 
        
        
        
        return (ydata,xdata)
        
    def get_attribute_names(self):
        
        return list(self.project_df.columns.values)
        

    def get_subjects_names(self):
        try:
            return self.subjects_df['name']
        except AttributeError:
            return []

    def get_subjects_names_by_group_id(self, group_id):
        return self.subjects_df["name"][self.subjects_df["group"]==group_id].tolist()

    def update_groups(self, group1_list, group2_list):
        for name in group1_list:
            self.subjects_df.ix[self.subjects_df["name"]==name,"group"]=[0]
        for name in group2_list:
            self.subjects_df.ix[self.subjects_df["name"]==name,"group"]=[1]
        
    
    def subjects_names_to_id(self, subjects_names):
        ids = []
        for name in subjects_names:
            ids.append(self.subjects_df["id"][self.subjects_df["name"]==name].tolist()[0])
        return ids
    def get_subject_name_by_id(self, subject_id):
        return self.subjects_df["name"][self.subjects_df["id"]==subject_id].tolist()[0]
        #for subject_name in group1_list:
        #    [subject for subject in self.subjects if subject.name == subject_name] 
    def get_group_by_subject_id(self, subject_id):
        return self.subjects_df["group"][self.subjects_df["id"]==subject_id].tolist()[0]