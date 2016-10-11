# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:13:49 2016

@author: Simulacrum
"""
import numpy as np

import sys

import sqlite3 as db

import pickle

from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.QtCore import Qt
import project_class


class Main_window(QMainWindow):
    
    def __init__(self, ):
        super().__init__()
        
        self.initUI()
        self.project = None
        
    def initUI(self):               
      
#        self.textEdit = QTextEdit()
#
#        self.setCentralWidget(self.textEdit)
        self.ncurves = 0
        self.chart = QChart()
        self.chart.legend().hide()
        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(self.view)
        
        
        #npoints = 10
        #xdata = [x * 10 / npoints for x in list(range(0, npoints))]
        #self.add_plot(xdata, np.sin(xdata), color=Qt.red)

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
        #toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('TeleVisor')
        self.setWindowIcon(QIcon('icons/show.png')) 
        self.show()
    def on_test(self):
        ydata = self.project.get_attribute_data(0)
        ydata = [ydata_p[0] for ydata_p in ydata if ydata_p[0]<5000 and ydata_p[0]>0 ]
        xdata = list(range(1,len(ydata)+1))
        self.add_plot(xdata, ydata, color=Qt.red)
    def on_add(self):
        fname = QFileDialog.getOpenFileNames(self, 'Add subject data', '',"Subject data (*.xls)")

        if fname[0]:
            for name in fname[0]:
                self.project.add_data(name)
                
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
        project_path = QFileDialog.getSaveFileName(self, "Create project","","TeleVisor project (*.prj)");
        if project_path[0]:
            self.project = project_class.Project_data(project_path[0]) 
        
                # Create empty database file
            db_con = db.connect(project_path[0][:-3]+"db")
            db_con.close()
        # Write the project file
            with open(project_path[0], 'wb') as f:
                pickle.dump(self.project, f)  
            
            self.add_dataAction.setDisabled(False)
            
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