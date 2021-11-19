#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from functools import partial
from collections import OrderedDict

import pandas as pd
import numpy as np

import math
import os
import pickle
import re
import shutil


class PrettyWidget(QMainWindow):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowState(Qt.WindowMaximized)
        #self.center()
        self.setWindowTitle('Import')

        self.scroll = QScrollArea()
        self.widget = QWidget()  
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)

        self.date_cb = QComboBox()
        self.date_cb.addItem('05052021', 0)
        self.date_cb.addItem('05042021', 1)
        self.date_cb.addItem('05032021', 2)
        #self.date_cb.currentIndexChanged.connect(self.selectionchange)
        self.grid.addWidget(self.date_cb, 0, 0)

        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit.setDisplayFormat("ddmmyyyy")
        self.grid.addWidget(self.dateEdit, 1, 0)

        self.createDate_button = QPushButton('Create date folder', self)
        self.createDate_button.clicked.connect(self.onclick_createDate)
        self.grid.addWidget(self.createDate_button, 2, 0)

        self.parent_dir = "..//SV_Data"

        '''
        self.fedtopic_arr, self.fedtopic_path_arr = self.get_fedtopic_filepath(self.dates_arr[0])
        for fedtopic in self.fedtopic_path_arr:
            fedname_arr, filepath_arr = self.get_fed_filepath(fedtopic)
             for fed in filepath_arr:
                model_data_arr.append(self.get_data(fed))
        '''


        #self.openFileNameDialog()
        #self.saveFileDialog()

        '''
        arr = self.openFileNamesDialog()
        for path in arr:
            newPath = shutil.copy(path, '..//SV_Data//abc', follow_symlinks=False)
        '''      
  
        
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
    
        self.show()

    def onclick_createDate(self,event):
        temp_var = self.dateEdit.date().toString('ddMMyyyy')
        path = os.path.join(self.parent_dir, temp_var)
        os.mkdir(path)


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
        return files
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setOptions(options)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def get_dates(self):
        date_arr = []
        basepath = '..\\SV_Data'+'\\'
        for date in os.listdir(basepath):
          date_arr.append(date)
        return date_arr

    def get_fedtopic(self,selected_date):
        fedtopic_arr = []
        basepath = '..\\SV_Data'+'\\'+selected_date+'\\'
        for fed_topic in os.listdir(basepath):
          fedtopic_arr.append(fed_topic)
        return fedtopic_arr

    def get_fed(self,selected_date,fedtopic):
        fedname_arr = []
        basepath = '..\\SV_Data'+'\\'+selected_date+'\\'+fedtopic+'\\'
        for fed in os.listdir(basepath):
          fedname_arr.append(fed)
        return fedname_arr


if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.aboutToQuit.connect(app.deleteLater)
  GUI = PrettyWidget()
  GUI.showMaximized()
  sys.exit(app.exec_())



#file dialog
#https://pythonspot.com/pyqt5-file-dialog/

#copy file
#https://thispointer.com/python-how-to-copy-files-from-one-location-to-another-using-shutil-copy/

#date edit format date
#https://www.geeksforgeeks.org/pyqt5-qdatetimeedit-setting-display-format/
#https://stackoverflow.com/questions/29428115/change-the-format-of-a-qdate