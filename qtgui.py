# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:13:49 2016

@author: Simulacrum
"""


import sys

import pyqtgraph



import pickle

from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMessageBox, QComboBox, QListWidget, QDockWidget, QAbstractItemView, QDialog, QPushButton  
from PyQt5.QtGui import QIcon

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

import project_class

from stats_widget import stats_dialog
from project_settings_dialog import project_settings_dialog


class Main_window(QMainWindow):
    
    def __init__(self, ):
        super().__init__()
        
        self.initUI()
        
        self.init_palette()
        self.project = None
        self.averaging = False
        self.current_project_path = ""
        
    def initUI(self):               
      

        self.subjects_listbox = QListWidget()
        self.subjects_listbox.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.subjects_listbox.itemSelectionChanged.connect(self.on_change_subjects)
        self.subjects_list_widget = QDockWidget("Subjects", self)
    
        self.subjects_list_widget.setAllowedAreas(Qt.LeftDockWidgetArea|
        Qt.RightDockWidgetArea)
        
        self.subjects_list_widget.setWidget(self.subjects_listbox)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.subjects_list_widget)
        
        self.stats_dialog = stats_dialog()
        self.stats_widget = QDockWidget("Statistics", self)
        self.stats_widget.setAllowedAreas(Qt.LeftDockWidgetArea|
        Qt.RightDockWidgetArea)
        self.stats_widget.setWidget(self.stats_dialog)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.stats_widget)
        
        self.ncurves = 0
        

        self.main_plot = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.main_plot)    
        

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
        
        self.settingsAction = QAction(QIcon('icons/settings.png'), 'Project settings', self)
        self.settingsAction.triggered.connect(self.on_project_settings)
        
        self.add_dataAction = QAction(QIcon('icons/add.png'), 'Add data', self)
        self.add_dataAction.setShortcut('Ctrl+a')
        self.add_dataAction.setStatusTip('Add data')
        self.add_dataAction.triggered.connect(self.on_add)
        self.add_dataAction.setDisabled(True)
        
        self.averageAction = QAction(QIcon('icons/average.png'), 'Average signal', self)
        self.averageAction.triggered.connect(self.on_average)
        
        self.aboutAction =  QAction(QIcon('icons/average.png'), 'About TeleVisor...', self)
        self.aboutAction.triggered.connect(self.on_about)
        
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
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(self.aboutAction)

        toolbar = self.addToolBar('Main toolbar')
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(self.add_dataAction)
        toolbar.addAction(self.settingsAction)
        toolbar.addAction(self.averageAction)
        toolbar.addWidget(self.combo_box_attribute)
        #toolbar.addAction(exitAction)
        
        self.setGeometry(200, 200, 950, 750)
        self.setWindowTitle('TeleVisor')
        self.setWindowIcon(QIcon('icons/show.png')) 
        self.show()
     
        
    def on_about(self):
        self.stats_dialog.average=1
        self.stats_dialog.update()
        QMessageBox.about(self,"About TeleVisor","TeleVisor 0.56 \n\nDeveloped by Dmitry Kamaev\n\nkdsw@yandex.ru")
    def on_test(self):        
        pass
    def on_average(self):
        if self.averaging == False:
            self.averaging = True
        else:
            self.averaging = False
        self.update_plot()
    def on_change_subjects(self):
        self.update_plot()
        
    def on_project_settings(self):
        group1_list = self.project.get_subjects_names_by_group_id(0)
        group2_list = self.project.get_subjects_names_by_group_id(1)
        dialog = project_settings_dialog(group1_list, group2_list)
        if dialog.exec():
            self.project.update_groups(dialog.group1_list,dialog. group2_list)
            self.update_plot()
         
    def update_plot(self):
        try:
            cold_color_counter = 0
            warm_color_counter = 0
            subjects_selected = [item.text() for item in self.subjects_listbox.selectedItems()]
            selected_subjects_ids = self.project.subjects_names_to_id(subjects_selected)
            attribute_name = self.project.get_attribute_names()[self.combo_box_attribute.currentIndex()]
            
            
            self.main_plot.clear()
            
            
            for subject_id in selected_subjects_ids:
                ydata = self.project.get_attribute_data(subject_id, attribute_name)
                xdata = self.project.get_attribute_data(subject_id, '_time')
                
                group = self.project.get_group_by_subject_id(subject_id)
                if group == 0:
                    plot_pen = pyqtgraph.mkPen(self.warm_palette[warm_color_counter])
                    warm_color_counter += 1
                elif group == 1:
                    plot_pen = pyqtgraph.mkPen(self.cold_palette[cold_color_counter])
                    cold_color_counter += 1
                            
                self.main_plot.plot(xdata, ydata, pen=plot_pen, name = self.project.get_subject_name_by_id(subject_id))
                
        except TypeError:
            self.main_plot.clear()
        if self.averaging == True:
            try:
                cold_color_counter = 0
                warm_color_counter = 0
                subjects_selected = [item.text() for item in self.subjects_listbox.selectedItems()]
                selected_subjects_ids = self.project.subjects_names_to_id(subjects_selected)
                attribute_name = self.project.get_attribute_names()[self.combo_box_attribute.currentIndex()]
                
                self.main_plot.clear()
                
                for subject_id in selected_subjects_ids:
                    ydata = self.project.get_averaged_attribute_data(subject_id, attribute_name)[0]
                    xdata = self.project.get_averaged_attribute_data(subject_id, attribute_name)[1]
                    
                    group = self.project.get_group_by_subject_id(subject_id)
                    if group == 0:
                        plot_pen = pyqtgraph.mkPen(self.warm_palette[warm_color_counter])
                        plot_brush = pyqtgraph.mkBrush(self.warm_palette[warm_color_counter])
                        warm_color_counter += 1
                    elif group == 1:
                        plot_pen = pyqtgraph.mkPen(self.cold_palette[cold_color_counter])
                        plot_brush = pyqtgraph.mkBrush(self.cold_palette[cold_color_counter])
                        cold_color_counter += 1
                                
                    self.main_plot.plot(xdata, ydata, pen=plot_pen,symbol = 'o',symbolBrush = plot_brush)
                    
            except TypeError:
                self.main_plot.clear()
            
            #self.main_plot.getAxis("bottom").setLogMode(True)
            #self.main_plot.hideAxis("bottom")
            
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
        
    def on_new(self):
        project_path = QFileDialog.getSaveFileName(self, "Create project","","TeleVisor project (*.prj)");
        if project_path[0]:
            self.project = project_class.Project_data(project_path[0]) 
            self.current_project_path = project_path[0]
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
                    
    def update_subjects_listbox(self):
        self.subjects_listbox.clear()
        self.subjects_listbox.addItems(self.project.get_subjects_names())
        
    def init_palette(self):
        self.warm_palette = [QColor(255,171,0),QColor(255,127,0),QColor(255,55,1),QColor(211,1,76),QColor(168,0,109)]
        self.cold_palette = [QColor(183,210,211),QColor(109,169,195),QColor(42,104,141),QColor(38,63,93),QColor(19,31,45)]
            
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Main_window()
    sys.exit(app.exec_())