# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 01:32:55 2016

@author: Simulacrum
"""

from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QDialog, QPushButton  
from PyQt5.QtGui import QIcon
class project_settings_dialog(QDialog):
    def __init__(self, group1_list,group2_list,):
        super().__init__()
        self.group1_list = group1_list
        self.group2_list = group2_list
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Project settings")
        self.setWindowIcon(QIcon('icons/settings.png'))
        self.setGeometry(200,200,610, 250)
        
        self.subjects_listbox_group1 = QListWidget(self)
        self.subjects_listbox_group1.move(10,10)
        self.subjects_listbox_group1.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.subjects_listbox_group1.addItems(self.group1_list)
        
        self.subjects_listbox_group2 = QListWidget(self)
        self.subjects_listbox_group2.move(315,10)
        self.subjects_listbox_group2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.subjects_listbox_group2.addItems(self.group2_list)
        
        to_group1_button = QPushButton("<<<",self)
        to_group1_button.move(270,100)
        to_group1_button.resize(40,25)
        to_group1_button.clicked.connect(self.to_group1)
        
        to_group2_button = QPushButton(">>>",self)
        to_group2_button.move(270,70)
        to_group2_button.resize(40,25)
        to_group2_button.clicked.connect(self.to_group2)
        
        ok_button = QPushButton("OK",self)
        ok_button.move(350,215)
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel",self)
        cancel_button.move(450,215)
        cancel_button.clicked.connect(self.reject)
        
    def to_group1(self):
        selected_in_group2 = [item.text() for item in self.subjects_listbox_group2.selectedItems()]
        
        self.group1_list.extend(selected_in_group2)
        for item in selected_in_group2:
            self.group2_list.remove(item)
        
        self.update_listboxes()
    
    def to_group2(self):
        
        selected_in_group1 = [item.text() for item in self.subjects_listbox_group1.selectedItems()]
        
        self.group2_list.extend(selected_in_group1)
        for item in selected_in_group1:
            self.group1_list.remove(item)
        
        self.update_listboxes()
        
    def update_listboxes(self):
        self.subjects_listbox_group1.clear()
        self.subjects_listbox_group2.clear()
        
        self.subjects_listbox_group1.addItems(self.group1_list)
        self.subjects_listbox_group2.addItems(self.group2_list)