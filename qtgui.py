# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:13:49 2016

@author: Simulacrum
"""


import sys


import sqlite3 as db
import os

import pickle

import time



from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

import project_class



        
 
        

class Main_window(QMainWindow):
    
    def __init__(self, ):
        super().__init__()
        
        self.initUI()
        self.project = None
        
    def initUI(self):               
        
        self.textEdit = QTextEdit()

        self.setCentralWidget(self.textEdit)

        openAction = QAction(QIcon('icons/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Project')
        openAction.triggered.connect(self.on_open)
        
        newAction = QAction(QIcon('icons/new_project.png'), 'New project', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip("Create new project")
        newAction.triggered.connect(self.on_new)
        
        
        self.add_dataAction = QAction(QIcon('icons/add.png'), 'Add data', self)
        self.add_dataAction.setShortcut('Ctrl+a')
        self.add_dataAction.setStatusTip('Add data')
        self.add_dataAction.triggered.connect(self.on_add)
        self.add_dataAction.setDisabled(True)
        
        
        exitAction = QAction(QIcon('icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Show Graph')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(self.add_dataAction)
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Main toolbar')
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(self.add_dataAction)
        #toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('TeleVisor')
        self.setWindowIcon(QIcon('icons/show.png')) 
        self.show()
    
    def on_add(self):
        fname = QFileDialog.getOpenFileNames(self, 'Add subject data', '',"Subject data (*.xls)")

        if fname[0]:
            self.project.add_data(fname[0][0])
                
    def on_open(self):
        if self.project is None:
            fname = QFileDialog.getOpenFileName(self, 'Open project', '',"TeleVisor project (*.prj)")

            if fname[0]:
                with open(fname[0], 'rb') as f:    
                    self.project = pickle.load(f)
                self.add_dataAction.setDisabled(False)
        else:
            reply = QMessageBox.question(self, 'Warning',
            "A project is already open. Close and save it?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                
                self.project = None
                self.on_open()
            else:
                pass
            #csv_from_excel(fname[0][0])
#            f = open(fname[0][0], 'r') # Opens first file only
#
#            with f:
#                
#                data = f.read()
#                self.textEdit.setText(data)     
        
    def on_new(self):
        project_path = QFileDialog.getSaveFileName(self, "Create project",
                           "","TeleVisor project (*.prj)");
        self.project = project_class.Project_data(project_path) 
        
                # Create empty database file
        db_con = db.connect(project_path[0][:-3]+"db")
        db_con.close()
        # Write the project file
        with open(project_path[0], 'wb') as f:
            pickle.dump(self.project, f)  
            
        self.add_dataAction.setDisabled(False)



#sh.row_values(rownum))
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())