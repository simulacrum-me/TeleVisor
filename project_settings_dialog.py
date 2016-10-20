# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 01:32:55 2016

@author: Simulacrum
"""

from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QDialog, QPushButton  
from PyQt5.QtGui import QIcon
class project_settings_dialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Project settings")
        self.setWindowIcon(QIcon('icons/settings.png'))
        self.setGeometry(200,200,650, 450)
        
        subjects_listbox_group1 = QListWidget(self)
        subjects_listbox_group1.move(10,10)
        subjects_listbox_group1.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        subjects_listbox_group2 = QListWidget(self)
        subjects_listbox_group2.move(315,10)
        subjects_listbox_group2.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        to_group1_button = QPushButton("<<<",self)
        to_group1_button.move(270,100)
        to_group1_button.resize(40,25)
        
        to_group2_button = QPushButton(">>>",self)
        to_group2_button.move(270,70)
        to_group2_button.resize(40,25)