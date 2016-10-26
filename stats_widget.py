# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 01:32:55 2016

@author: Simulacrum
"""

from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QDialog, QPushButton, QLabel, QGridLayout  
from PyQt5.QtGui import QIcon
class stats_dialog(QDialog):
    def __init__(self,):
        super().__init__()
        self.selected_average = 0
        self.selected_sd = 0
        
        self.gr1_average = 0
        self.gr1_sd = 0
        
        self.gr2_average = 0
        self.gr2_sd = 0
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle("Statistics")
        
        self.grid = QGridLayout()
        #self.setWindowIcon(QIcon('icons/settings.png'))
        #self.setGeometry(200,200,610, 250)
        
        
        
        
        
        self.average_label = QLabel(text = str(self.selected_average))
        self.sd_label = QLabel(text = str(self.selected_sd))
        
        self.gr1_average_label = QLabel(text = str(self.gr1_average))
        self.gr1_sd_label = QLabel(text = str(self.gr1_sd))
        
        self.gr2_average_label = QLabel(text = str(self.gr2_average))
        self.gr2_sd_label = QLabel(text = str(self.gr2_sd))
        
        self.grid.addWidget(QLabel(text = "Selected average:"),1,1)
        self.grid.addWidget(QLabel(text = "Selected SD:"),2,1)
        
        self.grid.addWidget(QLabel(text = "Selected group 1 average:"),3,1)
        self.grid.addWidget(QLabel(text = "Selected group 1 SD:"),4,1)
        
        self.grid.addWidget(QLabel(text = "Selected group 2 average:"),5,1)
        self.grid.addWidget(QLabel(text = "Selected group 2 SD:"),6,1)
        
        
        
        self.grid.addWidget(self.average_label,1,2)
        self.grid.addWidget(self.sd_label,2,2)
        
        self.grid.addWidget(self.gr1_average_label,3,2)
        self.grid.addWidget(self.gr1_sd_label,4,2)
        
        self.grid.addWidget(self.gr2_average_label,5,2)
        self.grid.addWidget(self.gr2_sd_label,6,2)
        
        
        
        self.setLayout(self.grid)
    def update(self):
        
        self.average_label.setText(str(self.selected_average))
        self.sd_label.setText(str(self.selected_sd))
        
        self.gr1_average_label.setText(str(self.gr1_average))
        self.gr1_sd_label.setText(str(self.gr1_sd))
        
        self.gr2_average_label.setText(str(self.gr2_average))
        self.gr2_sd_label.setText(str(self.gr2_sd))
        
        
        
#    def to_group1(self):
#        selected_in_group2 = [item.text() for item in self.subjects_listbox_group2.selectedItems()]
#        
#        self.group1_list.extend(selected_in_group2)
#        for item in selected_in_group2:
#            self.group2_list.remove(item)
#        
#        self.update_listboxes()
#    
#    def to_group2(self):
#        
#        selected_in_group1 = [item.text() for item in self.subjects_listbox_group1.selectedItems()]
#        
#        self.group2_list.extend(selected_in_group1)
#        for item in selected_in_group1:
#            self.group1_list.remove(item)
#        
#        self.update_listboxes()
#        
#    def update_listboxes(self):
#        self.subjects_listbox_group1.clear()
#        self.subjects_listbox_group2.clear()
#        
#        self.subjects_listbox_group1.addItems(self.group1_list)
#        self.subjects_listbox_group2.addItems(self.group2_list)