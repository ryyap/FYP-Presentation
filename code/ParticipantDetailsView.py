#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from functools import partial
import numpy as np
import math
import pandas as pd
from datetime import datetime

import FederatedModelView
import PDV_TableModel
import PDV_Controller

class PrettyWidget(QMainWindow):
    def __init__(self, fpid=103):
        super(PrettyWidget, self).__init__()
        self.initUI(fpid)

    def initUI(self,fpid):

        self.setWindowState(Qt.WindowMaximized)
        #self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle(str(fpid))

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)
        self.ind_lbl = QLabel("Participant: {}".format(str(fpid)), self)
        #a = QFont('Arial', 10)
        #self.ind_lbl.setFont(QtGui.QFont('Arial', 10))
        self.ind_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        self.grid.addWidget(self.ind_lbl, 0, 0, 1, 2)

        self.search_grid = QGridLayout()
        intermediateWidget = QWidget(self.widget)
        #intermediateWidget.setStyleSheet("border: 1px solid black;")
        intermediateWidget.setLayout(self.search_grid)
        intermediateWidget.setFixedWidth(400)

        self.grid.addWidget(intermediateWidget, 1, 1)
        self.table = QTableView()

        self.header = ['Date', 'Fed Name', 'Round', 'Performance', 'Contribution Value', 'Contribution%']
        self.selected_date = ''
        self.selected_fedtopic = ''


        self.curr_arr = []
        datetime_arr = []
        self.fid_arr = []
        self.last_round_contr_arr = []
        self.fedtopic_arr = []
        self.selected_date = 0
        self.selected_fedtopic = 0
        self.date_topic_arr = []

        controller = PDV_Controller.Controller(fpid)

        self.last_round_contr_arr = controller.last_round_contr_arr
        self.fid_arr = controller.fid_arr
        self.fedtopic_arr = controller.fedtopic_arr
        self.curr_arr = controller.curr_arr
        datetime_arr = controller.datetime_arr
            
        self.selected = 0;
        self.table_data = 0;

        self.figure1 = matplotlib.figure.Figure(figsize=(6,6))
        self.canvas1 = FigureCanvas(self.figure1)
        #self.plot1(self.data[0],self.fedname_arr)
        self.plot1(self.last_round_contr_arr[0][0], self.fid_arr[0][0], self.fedtopic_arr[0][0])
        self.canvas1.mpl_connect('button_press_event', self.onclick_round)
        self.grid.addWidget(self.canvas1, 1, 0)

        self.date_label = QLabel("Date:")
        self.date_cb = QComboBox()
        
        for x in range (len(datetime_arr)):
            self.date_cb.addItem(datetime_arr[x][0][0][0], x)
        #partial
        self.date_cb.currentIndexChanged.connect(partial(self.date_selectionchange)) 

        #print(fedtopic_arr[0])
        self.fedtopic_label = QLabel("Fed Topic:")
        self.fedtopic_cb = QComboBox()
        for x in range(len(self.fedtopic_arr[0])):
            self.fedtopic_cb.addItem(self.fedtopic_arr[0][x],x)
        self.fedtopic_cb.currentIndexChanged.connect(self.fedtopic_selectionchange)
        
        self.pfm_label = QLabel("Performance:")
        self.pfm_tb = QLineEdit(self)
        self.pfm_tb.setText('0.50')
        self.display_button = QPushButton('Display Selected', self)
        self.display_button.clicked.connect(self.onclick_displaySelected)
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.onclick_reset)

        pfm_validator = QRegExpValidator(QRegExp("0\.[0-9]{0,3}"))
        self.pfm_tb.setValidator(pfm_validator)

        self.search_grid.addWidget(self.date_label, 0, 0)
        self.search_grid.addWidget(self.date_cb, 0, 1)
        self.search_grid.addWidget(self.fedtopic_label, 1, 0)
        self.search_grid.addWidget(self.fedtopic_cb, 1, 1)
        self.search_grid.addWidget(self.pfm_label, 3, 0)   
        self.search_grid.addWidget(self.pfm_tb, 3, 1)  
        self.search_grid.addWidget(self.display_button, 4, 1)  
        self.search_grid.addWidget(self.reset_button, 5, 1)  
        
        
        self.table_data = self.curr_arr[0][0]
        self.model = PDV_TableModel.TableModel(self.table_data, self.header)
        self.table.setModel(self.model)
        self.table.setMinimumWidth(1800)
        self.table.setMinimumHeight(400)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True) 
        header.setSectionResizeMode(QHeaderView.Stretch) 
        self.grid.addWidget(self.table, 2, 0, 1, 4)
        

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.show()

    '''
    def get_pickle_data(self):
        filepath = "..\\SV_DB\\dbs_v2.pkl"
        file = open( filepath, "rb")
        object = pickle.load(file)
        return object
    '''

    '''
    def format_data(self,data):
      f_data = []
      for fed in data:
              for x in range(len(fed)):
                #print(fed[x])
                f_data.append(fed[x])
      return f_data
    '''

    def date_selectionchange(self, selected):
        self.selected_date = selected
        self.table_data = self.curr_arr[selected][0]
        self.model = ODV_TableModel.TableModel(self.table_data, self.header)
        self.table.setModel(self.model)

        if self.fedtopic_cb.count() > 0:
            self.fedtopic_cb.currentIndexChanged.disconnect() 
            self.fedtopic_cb.clear()
            
        for x in range(len(self.fedtopic_arr[selected])):
            self.fedtopic_cb.addItem(self.fedtopic_arr[selected][x],x)
        self.fedtopic_cb.currentIndexChanged.connect(self.fedtopic_selectionchange)
        #self.plot1(self.data[selected],self.fedname_arr)
        self.plot1(self.last_round_contr_arr[selected][0],self.fid_arr[selected][0], self.fedtopic_arr[selected][0])


    def fedtopic_selectionchange(self, selected):
        
        self.selected_fedtopic = selected
        self.table_data = self.curr_arr[self.selected_date][selected]
        self.model = PDV_TableModel.TableModel(self.table_data, self.header)
        self.table.setModel(self.model)
        #self.plot1(self.data[selected],self.fedname_arr)
        self.plot1(self.last_round_contr_arr[self.selected_date][selected],self.fid_arr[self.selected_date][selected], 
            self.fedtopic_arr[self.selected_date][selected])

    def onclick_round(self,event):
        x1 = event.xdata
        x2 = 0
        #print('x1: ', x1)
        if isinstance(x1, float):
          if x1 > 0:
            x2 = round(x1)
            x2 = int(x2)
        print(x2)
        df = pd.DataFrame(self.curr_arr[self.selected_date][self.selected_fedtopic])
        #print(df)
        #print(df[df[1]==x2])
        fid_arr = df[1].unique()
        #print(fid_arr)
        table_data = df[df[1]==fid_arr[x2]].values.tolist()
        self.model = PDV_TableModel.TableModel(table_data, self.header)
        self.table.setModel(self.model)

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Open Model")
        self.msg.setText("Do you want to open model?")
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        button = self.msg.exec()
        if button == QMessageBox.Yes:
            print("Yes!")
            #self.panel = Model.PrettyWidget(self.selected_date, self.selected_fedtopic,self.fedname_arr[x2])
            self.panel = FederatedModelView.PrettyWidget(table_data[0][1])
        else:
            print("No!")
        self.msg.buttonClicked.connect(self.popup_button)

    def popup_button(self, i):
        print('i')


    def onclick_displaySelected(self):

      pfm = self.pfm_tb.text()
      data = self.curr_arr[self.selected_date][self.selected_fedtopic]
      df = pd.DataFrame(data)
      table_data = df[df[3]>=float(pfm)].values.tolist()


      if(table_data!=[]):
        #print(data)
        self.model = PDV_TableModel.TableModel(table_data, self.header)
        self.table.setModel(self.model)
      else:
        #self.table.reset();
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("No data")
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def onclick_reset(self):
      self.table_data = self.curr_arr[self.selected_date][self.selected_fedtopic]
      self.model = PDV_TableModel.TableModel(self.table_data, self.header)
      self.table.setModel(self.model)
      #self.plot1(self.data[selected])
      self.plot1(self.last_round_contr_arr[self.selected_date][self.selected_fedtopic], 
        self.fid_arr[self.selected_date][self.selected_fedtopic], 
        self.fedtopic_arr[self.selected_date][self.selected_fedtopic])

                
    def plot1(self,data,fedname_arr,fedtopic):
        self.figure1.clf()
        ax1 = self.figure1.add_subplot(111) 

        fed = []
        contribution = []

        arr = []
        for fed in fedname_arr:
            arr.append(fedtopic + str(fed))
        #print(arr)

        ind = np.arange(len(arr))
        if len(arr) == 1:
            bar_width = 0.001
        else:
            bar_width = 0.2

        ax1.bar(ind, data,  width=bar_width)
        ax1.set_xticks(ind)
        ax1.set_xticklabels(arr)
        ax1.set_ylabel("Contribution")
        ax1.set_xlabel("Federation")
        ax1.set_title("{}".format(fedtopic))
        self.canvas1.draw_idle()


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

#model + table
#https://www.mfitzp.com/tutorials/qtableview-modelviews-numpy-pandas/

#vbox layout
#https://www.tutorialspoint.com/pyqt/pyqt_qboxlayout_class.htm

#add another layout to gridlayout
#http://srinikom.github.io/pyside-docs/PySide/QtGui/QGridLayout.html#PySide.QtGui.PySide.QtGui.QGridLayout.addLayout

#button
#https://pythonspot.com/pyqt5-buttons/

#set table height and width
#https://linuxhint.com/use-pyqt-qtablewidget/

#stretch table column
#https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a

#button on click pass variable
#https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt/42945033

#popup
#https://www.techwithtim.net/tutorials/pyqt5-tutorial/messageboxes/

#dialog box
#https://www.mfitzp.com/tutorials/pyqt-dialogs/

#delete df col
#https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe

#get word after word match
#https://stackoverflow.com/questions/5006716/getting-the-text-that-follows-after-the-regex-match 