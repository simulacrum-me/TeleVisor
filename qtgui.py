# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:13:49 2016

@author: Simulacrum
"""
import numpy as np

import sys

import sqlite3 as db

import pickle

from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMessageBox, QComboBox, QListWidget, QDockWidget, QAbstractItemView  
from PyQt5.QtGui import QIcon

from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter, QColor
from PyQt5.QtCore import Qt
import project_class


class Main_window(QMainWindow):
    
    def __init__(self, ):
        super().__init__()
        
        self.initUI()
        
        self.init_palette()
        self.project = None
        self.current_project_path = ""
        
    def initUI(self):               
      
#        self.textEdit = QTextEdit()
#
#        self.setCentralWidget(self.textEdit)
        self.subjects_listbox = QListWidget()
        self.subjects_listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.subjects_listbox.itemSelectionChanged.connect(self.on_change_subjects)
        self.subjects_list_widget = QDockWidget("Subjects", self)
        #self.subjects_list_widget.setObjectName("LogDockWidget")
        self.subjects_list_widget.setAllowedAreas(Qt.LeftDockWidgetArea|
        Qt.RightDockWidgetArea)
        
        self.subjects_list_widget.setWidget(self.subjects_listbox)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.subjects_list_widget)

        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)

        openAction = QAction(QIcon('icons/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Project')
        openAction.triggered.connect(self.on_open)
        
        newAction = QAction(QIcon('icons/new_project.png'), 'New project', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip("Create new project")
        newAction.triggered.connect(self.on_new)
        
        self.plotAction = QAction(QIcon('icons/show.png'), 'Plot', self)
        self.plotAction.triggered.connect(self.on_test)
        
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
        self.combo_box_attribute = QComboBox()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(self.add_dataAction)
        fileMenu.addAction(self.plotAction)
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Main toolbar')
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(self.add_dataAction)
        toolbar.addWidget(self.combo_box_attribute)
        #toolbar.addAction(exitAction)
        
        self.setGeometry(200, 200, 950, 750)
        self.setWindowTitle('TeleVisor')
        self.setWindowIcon(QIcon('icons/show.png')) 
        self.show()
        
    def on_test(self):
        
        attribute_name = self.project.get_attribute_names()[self.combo_box_attribute.currentIndex()]
        color_warm_id = 0
        for subject in self.project.subjects:
            ydata = self.project.get_attribute_data(subject.id, attribute_name)
            ydata = [ydata_p[0] for ydata_p in ydata]
            xdata = list(range(1,len(ydata)+1))
            self.add_plot(xdata, ydata, color=self.warm_palette[color_warm_id])
            color_warm_id += 1
        
    def on_change_subjects(self):
        subjects_selected = [item.text() for item in self.subjects_listbox.selectedItems()]
        print(subjects_selected)
        selected_subjects_ids = [subject.id for subject in self.project.subjects if subject.name in subjects_selected]
        color_warm_id = 0
        attribute_name = self.project.get_attribute_names()[self.combo_box_attribute.currentIndex()]
        self.chart.removeAllSeries()
        for subject_id in selected_subjects_ids:
            ydata = self.project.get_attribute_data(subject_id, attribute_name)
            ydata = [ydata_p[0] for ydata_p in ydata]
            xdata = list(range(1,len(ydata)+1))
            self.add_plot(xdata, ydata, color=self.warm_palette[color_warm_id])
            color_warm_id += 1
        
        
    def on_add(self):
        fname = QFileDialog.getOpenFileNames(self, 'Add subject data', '',"Subject data (*.xls)")

        if fname[0]:
            for name in fname[0]:
                self.project.add_data(name)
            self.combo_box_attribute.addItems(self.project.get_attribute_names())
            self.update_subjects_listbox()   
            self.save_project(self.current_project_path)
            
    def on_open(self):
        if self.project is None:
            fname = QFileDialog.getOpenFileName(self, 'Open project', '',"TeleVisor project (*.prj)")

            if fname[0]:
                self.current_project_path = fname[0]
                self.load_project(self.current_project_path)
                self.add_dataAction.setDisabled(False)
                self.combo_box_attribute.addItems(self.project.get_attribute_names())
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
        project_path = QFileDialog.getSaveFileName(self, "Create project","","TeleVisor project (*.prj)");
        if project_path[0]:
            self.project = project_class.Project_data(project_path[0]) 
            self.current_project_path = project_path[0]
                # Create empty database file
            db_con = db.connect(project_path[0][:-3]+"db")
            db_con.close()
            # Write the project file
            self.save_project(project_path[0])
            self.add_dataAction.setDisabled(False)
            
    def save_project(self, path):
        with open(path, 'wb') as f:
                pickle.dump(self.project, f)  
    
    def load_project(self, path):
        with open(path, 'rb') as f:    
                    self.project = pickle.load(f)
                    self.update_subjects_listbox()
                    
    def add_plot(self, xdata, ydata, color=None):
        curve = QLineSeries()
        pen = curve.pen()
        if color is not None:
            pen.setColor(color)
        pen.setWidthF(.1)
        curve.setPen(pen)
        curve.setUseOpenGL(True)
        curve.append(series_to_polyline(xdata, ydata))
        self.chart.addSeries(curve)
        self.chart.createDefaultAxes()
        self.ncurves += 1
    def update_subjects_listbox(self):
        self.subjects_listbox.clear()
        self.subjects_listbox.addItems(self.project.get_subjects_names())
    def init_palette(self):
        self.warm_palette = [QColor(255,171,0),QColor(255,127,0),QColor(255,55,1),QColor(211,1,76),QColor(168,0,109)]
        self.cold_palette = [QColor(183,210,211),QColor(109,169,195),QColor(42,104,141),QColor(38,63,93),QColor(19,31,45)]

#sh.row_values(rownum))
def series_to_polyline(xdata, ydata):
    """Convert series data to QPolygon(F) polyline

    This code is derived from PythonQwt's function named 
    `qwt.plot_curve.series_to_polyline`"""
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2*polyline.size()*tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size-1)*2+1:2] = xdata
    memory[1:(size-1)*2+2:2] = ydata
    return polyline  
                
                
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())