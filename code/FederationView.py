#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui

import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from functools import partial
import numpy as np
import math
import pandas as pd
#import subprocess
import os
import pickle
from collections import OrderedDict
import re
import math
import glob
import sip

import FederatedModelView
import ParticipantReputationView
from DAO import FV_DAO

class PrettyWidget(QMainWindow):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):

        #self.setGeometry(100, 100, 800, 600)
        self.setWindowState(Qt.WindowMaximized)
        self.center()
        self.setWindowTitle('Federation')

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)
        self.hbox = QHBoxLayout()

        self.grid_arr = []
        self.dates_arr = []
        self.selected_date = ''

        self.fed_name_lbl = QLabel("Federations", self)
        self.fed_name_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        self.fed_name_lbl.setAlignment(Qt.AlignTop)
        self.fed_name_lbl.setMaximumHeight(60)
        #self.fed_name_lbl.setStyleSheet("border: 1px solid black;")
        self.rep_button = QPushButton('View Reputation', self)
        self.rep_button.clicked.connect(self.onclick_openReputation)
        self.rep_button.setFixedWidth(300)
        
        self.grid.addWidget(self.fed_name_lbl, 0, 0, 1, 2)
        self.grid.addWidget(self.rep_button, 0, 2, 1, 1)

        self.hbox1 = QHBoxLayout()
        #self.hbox1.setFixedWidth(300)


        self.date_lbl = QLabel("Date: ", self)
        self.date_lbl.setFixedWidth(100)

        self.date_cb = QComboBox()

        self.hbox1.addWidget(self.date_lbl)
        self.hbox1.addWidget(self.date_cb)

        self.hbox2 = QHBoxLayout()

        self.fedtopic_lbl = QLabel("Federation Topic: ", self)
        self.fedtopic_lbl.setFixedWidth(170)

        self.fedtopic_cb = QComboBox()
        #print('ft',self.fedtopic_arr)
        self.fedtopic_cb.setFixedWidth(250)

        self.hbox2.addWidget(self.fedtopic_lbl)
        self.hbox2.addWidget(self.fedtopic_cb)
        
        #self.hbox.addWidget(self.date_lbl)
        #self.hbox.addWidget(self.date_cb)
        #self.hbox.addWidget(self.fedtopic_lbl)
        #self.hbox.addWidget(self.fedtopic_cb)
        self.hbox.addLayout(self.hbox1)
        self.hbox.addLayout(self.hbox2)
        self.date_lbl.setAlignment(Qt.AlignHCenter )
        self.fedtopic_lbl.setAlignment(Qt.AlignHCenter )
        self.hbox.setAlignment(Qt.AlignHCenter )
        self.grid.addLayout(self.hbox,1, 0, 1, 4)

        dao = FV_DAO.DAO()

        #pickle_data = self.get_pickle_data()

        overall_data = dao.get_fed_overall_data()
        date_arr = overall_data['date'].unique()
        fedtopic_fid_df = dao.get_fedtopic_fid()
        overall_data = pd.merge(overall_data, fedtopic_fid_df, on='fid')

        data_arr = []
        for date in date_arr:
            temp_df = overall_data[(overall_data['date']==date)]
            temp_fedtopic_arr = temp_df['fedtopic'].unique()
            temp1 = []      
            for fedtopic in temp_fedtopic_arr:
                temp2 = []
                temp_df2 = temp_df[(overall_data['fedtopic']==fedtopic)]
                fed_arr = temp_df['fid'].unique()
                for fed in fed_arr:
                    temp_fed_df = temp_df2[(overall_data['fid']==fed)]
                    if not temp_fed_df.empty:
                        temp2.append(temp_fed_df[['fedtopic', 'fid', 'rid', 'acc','loss', 'date', 
                            'all participants']].to_numpy())
                temp1.append(temp2)
            data_arr.append(temp1)
        print(data_arr)

        #data_arr2.append(data_arr2[0])

        #self.dates_arr = self.get_dates()
        #data2 = self.get_data2()
        self.selected_date = data_arr[0][0][0][0][5]
        #self.load_data(self.dates_arr[0])
        self.load_overall_fed_data(data_arr[0])
        #print('l')
        #print(data_arr2[0][0][0][0][5])

        for x in range(len(data_arr)):
            self.date_cb.addItem(data_arr[x][0][0][0][5],x)
        self.date_cb.setFixedWidth(250)
        self.date_cb.currentIndexChanged.connect(partial(self.selectionchange_date,data_arr))

        #self.fedtopic_cb.currentIndexChanged.connect(partial(self.selectionchange_fedtopic,self.fedtopic_arr))

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)


        self.show()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def column(self, matrix, i):
        return [row[i] for row in matrix]

    def load_overall_fed_data(self,data):
        
        if(len(self.grid_arr)>0):
            print('delete fedtopic')
            for x in range(len(self.grid_arr)):
                self.clearLayout(self.grid_arr[x])

                widget = self.grid.itemAtPosition(x+2,0).widget()
                if widget is not None:
                    #widget.deleteLater()
                    widget.setParent(None)

                
                widget = self.grid.itemAtPosition(x+2,1).widget()
                if widget is not None:
                    widget.setParent(None)
            
        for x in range(2,10):
            print(x)
            item  = self.grid.itemAtPosition(x,0)
            if item is not None:
                item.deleteLater()

        if self.fedtopic_cb.count() > 0:
            self.fedtopic_cb.currentIndexChanged.disconnect() 
            self.fedtopic_cb.clear()

        self.grid_arr=[]
        self.canvas_arr = []
        self.figure_arr = []
        self.button_arr = []
        self.label_arr = []
        self.cb_arr = []
        label_box = []

        for x in range(len(data)):

          intermediateWidget = QWidget(self.widget)
          intermediateWidget.setStyleSheet("border: 1px solid black;padding: 10px;")
          intermediateWidget.setMaximumHeight(400)

    
          self.grid.addWidget(intermediateWidget, x+2, 0)
          glayout = QGridLayout()
          self.grid_arr.append(glayout)
          self.grid.addLayout(self.grid_arr[x],x+2,0)

          cb = QComboBox()
          fid_arr = []
          for item in data[x]:
              #print(item[0])
              cb.addItem(item[0][0] + ' ' + str(item[0][1]), x)
              fid_arr.append(item[0][1])
          cb.currentIndexChanged.connect(partial(self.selectionchange_model, data[x], x))
          cb.setFixedSize(100,30)
          self.cb_arr.append(cb)


          label_box = []
          label1 = QLabel("Data: %s" % (data[x][0][0][0]), self)
          #label1 = QLabel("Data:")
          label2 = QLabel("Model: ", self)  
          label3 = QLabel("Date: %s" % (data[x][0][-1][5]), self)
          #////
          #print("aaa")
          p = float("{:.4f}".format(data[x][0][-1][3]))
          label4 = QLabel("Performance: %s" % (p), self)
          label5 = QLabel("Contributors: %s" % (str(data[x][0][-1][6])), self)
          label6 = QLabel("Comment: ",self)
          label_box = [label1, label2, label3, label4, label5]
          self.label_arr.append(label_box)
          button = QPushButton('View Model', self)
          self.button_arr.append(button)
          self.button_arr[x].clicked.connect(partial(self.onclick_openModel, fid_arr, cb))

          self.grid_arr[x].addWidget(label1, 0, 0)
          self.grid_arr[x].addWidget(label2, 1, 0)
          self.grid_arr[x].addWidget(self.cb_arr[x],1, 1)
          self.grid_arr[x].addWidget(label3, 2, 0)
          self.grid_arr[x].addWidget(label4, 3, 0)
          self.grid_arr[x].addWidget(label5, 4, 0)
          self.grid_arr[x].addWidget(self.button_arr[x], 5, 0, 1, 2)

          acc = self.column(data[x][0], 3)
          loss = self.column(data[x][0], 4)

          figure = matplotlib.figure.Figure(figsize=(14,len(data)+1))
          self.figure_arr.append(figure) 
          canvas = FigureCanvas(self.figure_arr[x])
          self.canvas_arr.append(canvas)
          self.plot(acc, loss, self.figure_arr[x], self.canvas_arr[x])
          self.figure_arr[x].tight_layout()
          self.grid.addWidget(self.canvas_arr[x], x+2, 1, 1, 2)

        self.fedtopic_cb.addItem("Overall")

        #print(data[x])

        for item in data:
           self.fedtopic_cb.addItem(item[0][0][0])

        self.fedtopic_cb.currentIndexChanged.connect(partial(self.selectionchange_fedtopic,data))

        return

    def load_selected_fed_data(self,data,num_select):


          delete = 0
          print('delete topic')
          for x in range(len(self.grid_arr)):
                print(delete)
                delete += 1
                
                self.clearLayout(self.grid_arr[x])
                
                widget = self.grid.itemAtPosition(x+2,0).widget()
                if widget is not None:
                    widget.setParent(None)

                
                widget = self.grid.itemAtPosition(x+2,1).widget()
                if widget is not None:
                    widget.setParent(None)

          print('grid len')
          print(len(self.grid_arr))
          self.grid_arr=[]
          self.canvas_arr = []
          self.figure_arr = []
          self.button_arr = []
          self.label_arr = []
          self.cb_arr = []
          label_box = []

          #here
          #print('loop')
          for x in range(2,10):
            print(x)
            item  = self.grid.itemAtPosition(x,0)
            if item is not None:
                item.deleteLater()
          
          count = 0
          print('fedtopic count')
          print(count)
          intermediateWidget = QWidget(self.widget)
          intermediateWidget.setStyleSheet("border: 1px solid black;padding: 10px;")
          intermediateWidget.setMaximumHeight(400)
          self.grid.addWidget(intermediateWidget, 2, 0)
          glayout = QGridLayout()
          self.grid_arr.append(glayout)
          self.grid.addLayout(self.grid_arr[0],2,0)

          #print('o')
          #print(data[0][0])
          fid_arr = []

          cb = QComboBox()
          for item in data:
              cb.addItem(item[0][0] + ' ' + str(item[0][1]),num_select)
              fid_arr.append(item[0][1])
          cb.currentIndexChanged.connect(partial(self.selectionchange_model, data, 0))
          cb.setFixedSize(100,30)
          self.cb_arr.append(cb)

          label_box = []
          label1 = QLabel("Data: %s" % (data[0][0][0]), self)
          label2 = QLabel("Model: ", self)  
          label3 = QLabel("Date: %s" % (data[0][-1][5]), self)
          #///

          p = float("{:.4f}".format(data[0][-1][3]))
          label4 = QLabel("Performance: %s" % p, self)
          label5 = QLabel("Contributors: %s" % (str(data[0][-1][6])), self)
          label6 = QLabel("Comment: ",self)
          label_box = [label1, label2, label3, label4, label5]
          self.label_arr.append(label_box)
          button = QPushButton('View Model', self)
          self.button_arr.append(button)
          self.button_arr[0].clicked.connect(partial(self.onclick_openModel, fid_arr, cb))

          self.grid_arr[0].addWidget(label1, 0, 0)
          self.grid_arr[0].addWidget(label2, 1, 0)
          self.grid_arr[0].addWidget(self.cb_arr[0],1, 1)
          self.grid_arr[0].addWidget(label3, 2, 0)
          self.grid_arr[0].addWidget(label4, 3, 0)
          self.grid_arr[0].addWidget(label5, 4, 0)
          self.grid_arr[0].addWidget(self.button_arr[0], 5, 0, 1, 2)

          acc = self.column(data[0], 3)
          loss = self.column(data[0], 4)

          figure = matplotlib.figure.Figure(figsize=(15,4))
          self.figure_arr.append(figure) 
          #print(len(self.figure_arr))
          canvas = FigureCanvas(self.figure_arr[0])
          self.canvas_arr.append(canvas)
          self.plot(acc, loss, self.figure_arr[0], self.canvas_arr[0])
          self.figure_arr[0].tight_layout()
          self.grid.addWidget(self.canvas_arr[0], 2, 1, 1, 2)
          return

    def plot(self,acc_arr,loss_arr,figure,canvas):
        #print('plot')
        figure.clf()

        acc_arr = list(np.around(np.array(acc_arr),4))
        loss_arr = list(np.around(np.array(loss_arr),4))

        round_arr = []

        for x in range(len(acc_arr)):
            round_arr.append(x+1)

        ax1 = figure.add_subplot(121) 
        ax1.title.set_text('Accuracy Per Round')
        max_value = max(acc_arr)
        max_value = max_value + max_value*0.1
        min_value = min(acc_arr)
        min_value = min_value - min_value*0.1
        ax1.set_ylim(min_value, max_value)
        ax1.set(xlabel="Rounds", ylabel="Accuracy")
        ax1.plot(round_arr,acc_arr)
        # zip joins x and y coordinates in pairs
        for x,y in zip(round_arr,acc_arr):
                 ax1.annotate(y, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
        
        ax2 = figure.add_subplot(122) 
        ax2.title.set_text('Loss Per Round')
        max_value = max(loss_arr)
        max_value = max_value + max_value*0.1
        min_value = min(loss_arr)
        min_value = min_value - min_value*0.1
        ax2.set_ylim(min_value, max_value)
        ax2.set(xlabel="Rounds", ylabel="Loss")
        ax2.plot(round_arr,loss_arr)
        # zip joins x and y coordinates in pairs
        for x,y in zip(round_arr,loss_arr):
                 ax2.annotate(y, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
        

        canvas.draw_idle()
        return

    def onclick_openModel(self, fid, cb):
      index = cb.currentIndex()
      self.panel = FederatedModelView.PrettyWidget(fid[index])
      return
      #Model()

    def onclick_openReputation(self):
        self.panel = ParticipantReputationView.PrettyWidget()
        return

    def selectionchange_date(self, data_arr, x):

        print('date cb')
        print(x)
        self.selected_date = str( self.date_cb.currentText())
        self.load_overall_fed_data(data_arr[x])
        return

    def selectionchange_fedtopic(self, data, x):

        if(x>0):
            self.load_selected_fed_data(data[x-1],x-1)
        else:
            self.load_overall_fed_data(data)
        #self.load_data(dates_arr[x])
        return

    def selectionchange_model(self, data, fedtopic_index, i):
      
      acc_arr = self.column(data[i], 3)
      loss_arr = self.column(data[i], 4)
      self.label_arr[fedtopic_index][0].setText("Data: %s" %data[i][-1][0])
      #self.label_arr[fedtopic_index][1].setText("gg")
      self.label_arr[fedtopic_index][2].setText("Date: %s" % (data[i][-1][5]))
      p = float("{:.4f}".format(data[i][-1][3]))
      self.label_arr[fedtopic_index][3].setText("Performance: %s" % (p))
      self.label_arr[fedtopic_index][4].setText("Contributors: %s" % (str(data[i][-1][6])))

      self.plot(acc_arr, loss_arr, self.figure_arr[fedtopic_index], self.canvas_arr[fedtopic_index])

      return
      

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        return


if __name__ == "__main__":
  app = QApplication(sys.argv)
  app.aboutToQuit.connect(app.deleteLater)
  GUI = PrettyWidget()
  GUI.showMaximized()
  sys.exit(app.exec_())

#pyqt4 + matplotlib
#https://stackoverflow.com/questions/36086361/embed-matplotlib-in-pyqt-with-multiple-plot

#pyqt4 to pyqt5
#https://stackoverflow.com/questions/45501514/attributeerror-module-pyqt5-qtgui-has-no-attribute-qwidget

#maximize window
#https://www.geeksforgeeks.org/pyqt5-how-to-open-window-in-maximized-format/

#scrollbar
#https://www.mfitzp.com/tutorials/qscrollarea/

#columnspan / rowspan
#https://stackoverflow.com/questions/38325350/how-to-combine-columns-in-a-layout-colspan-feature

#update plot
#https://stackoverflow.com/questions/53258160/update-an-embedded-matplotlib-plot-in-a-pyqt5-gui-with-toolbar

#multi line label
#https://stackoverflow.com/questions/36412923/python-qt-and-multi-row-qlabel

#update label
#https://www.geeksforgeeks.org/pyqt5-how-to-change-text-of-pre-existing-label-settext-method/

#dropdown list
#https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm

#resize widget
#https://stackoverflow.com/questions/55663761/how-to-reduce-the-size-of-a-qcombobox-with-pyqt

#open script
#https://stackoverflow.com/questions/24327308/pyqt4-open-py-file-when-button-is-clicked

#widget inside a widget
#https://stackoverflow.com/questions/32461921/pyqt-qgridlayout-set-first-row-stylesheet

#border stylesheet
#https://stackoverflow.com/questions/21193729/pyqt-lineedit-border-color

#fullscreen
#https://stackoverflow.com/questions/15702470/how-to-make-a-window-that-occupies-the-full-screen-without-maximising

#pass data
#https://forum.qt.io/topic/112315/pyqt-pass-data-between-windows-and-run-script-in-second-window/7

#remove wideget from gridlayout
#https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
#https://stackoverflow.com/questions/60149456/is-there-any-way-to-delete-widget-by-its-position-in-grid-or-delete-row-in-this
#https://www.qtcentre.org/threads/30894-qgridlayout-and-hiding-widgets
#https://www.codenong.com/cs109718288/