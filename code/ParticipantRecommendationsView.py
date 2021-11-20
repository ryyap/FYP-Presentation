#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from functools import partial
import numpy as np
import math
import pandas as pd
from datetime import datetime
import csv

import PRV_TableModel
import PRV_InputDialog
import PRV_Controller
import ParticipantDetailsView
import PButtonDelegate

class PrettyWidget(QMainWindow):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):

        #self.setGeometry(100, 100, 800, 600)
        # self.center()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('Participant Recommendation')

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        # self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)

        self.feds = ['NLP', 'CV', 'IR']
        

        self.prec_lbl = QLabel("Participant Recommendation", self)
        self.prec_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        self.grid.addWidget(self.prec_lbl, 0, 0)

        self.widget1 = QWidget(self.widget)
        self.hbox1 = QHBoxLayout()
        self.widget1.setLayout(self.hbox1)
        self.widget1.setFixedWidth(400)
        self.grid.addWidget(self.widget1, 1, 0, 1, 1)

        self.widget2 = QWidget(self.widget)
        self.hbox2 = QHBoxLayout()
        self.widget2.setLayout(self.hbox2)
        self.widget2.setFixedWidth(400)
        self.grid.addWidget(self.widget2, 1, 1, 1, 1)

        self.widget3 = QWidget(self.widget)
        self.hbox3 = QHBoxLayout()
        self.widget3.setLayout(self.hbox3)
        self.widget3.setFixedWidth(850)
        self.grid.addWidget(self.widget3, 1, 2, 1, 2)

        self.widget4 = QWidget(self.widget)
        self.hbox4 = QHBoxLayout()
        self.widget4.setLayout(self.hbox4)
        self.widget4.setFixedWidth(500)
        self.grid.addWidget(self.widget4, 2, 0, 1, 1)
        #self.grid.addLayout(self.hbox1, 1, 0, 1, 1)

        self.widget5 = QWidget(self.widget)
        self.hbox5 = QHBoxLayout()
        self.widget5.setLayout(self.hbox5)
        self.widget5.setFixedWidth(250)
        self.grid.addWidget(self.widget5, 2, 1, 1, 1)
        #self.grid.addLayout(self.hbox2, 1, 1, 1, 1)

        self.widget6 = QWidget(self.widget)
        self.hbox6 = QHBoxLayout()
        self.widget6.setLayout(self.hbox6)
        self.widget6.setFixedWidth(400)
        self.grid.addWidget(self.widget6, 2, 2, 1, 1)
        #self.grid.addLayout(self.hbox3, 1, 2, 1, 1)

        self.widget7 = QWidget(self.widget)
        self.hbox7 = QHBoxLayout()
        self.widget7.setLayout(self.hbox7)
        self.widget7.setFixedWidth(350)
        self.grid.addWidget(self.widget7, 2, 3, 1, 1)

        self.table = QTableView()
        self.grid.addWidget(self.table, 4, 0, 1, 4)

        self.from_label = QLabel("Date From:")
        self.from_label.setFixedWidth(100)
        self.from_label.setAlignment(Qt.AlignLeft)
        date = QDate(2021, 7, 1)
        self.from_dateEdit = QDateEdit()
        self.from_dateEdit.setCalendarPopup(True)
        self.from_dateEdit.setDate(date)
        self.from_dateEdit.setFixedWidth(200)
        self.to_label = QLabel("Date To:")
        self.to_label.setFixedWidth(100)
        self.to_dateEdit = QDateEdit()
        self.to_dateEdit.setCalendarPopup(True)
        self.to_dateEdit.setDateTime(QDateTime.currentDateTime())
        self.to_dateEdit.setFixedWidth(200)
        self.hbox1.addWidget(self.from_label)
        self.hbox1.addWidget(self.from_dateEdit)
        self.hbox2.addWidget(self.to_label)
        self.hbox2.addWidget(self.to_dateEdit)

        self.rep_label = QLabel("Repuation:")
        self.rep_label.setFixedWidth(100)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(300)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(30)
        self.slider.setFixedWidth(600)
        self.rep_value_label = QLabel('10', self)
        self.rep_value_label.setFixedWidth(50)
        self.slider.valueChanged.connect(self.slider_valuechange)
        self.hbox3.addWidget(self.rep_label)
        self.hbox3.addWidget(self.slider)
        self.hbox3.addWidget(self.rep_value_label)

        self.fed_label = QLabel('Select Federation: ', self)
        self.fed_label.setFixedWidth(150)
        self.fed_cb = QComboBox()
        self.fed_cb.addItem('All',-1)
        self.fed_cb.addItem('Natural Processing Language (NLP)',0)
        self.fed_cb.addItem('Computer Vision (CV)',1)
        self.fed_cb.addItem('Image Recognition (IR)',2)
        self.fed_cb.setFixedWidth(300)
        self.hbox4.addWidget(self.fed_label)
        self.hbox4.addWidget(self.fed_cb)

        self.avail_check = QCheckBox("Show Available Only",self)
        self.hbox5.addWidget(self.avail_check)
        
        self.display_button = QPushButton('Display Selected', self)
        self.display_button.setFixedWidth(300)
        self.hbox7.addWidget(self.display_button)

        self.header = ['Select', 'Participant ID', 'Repuation', 'Federation Participated', 'Availability']

        from_date = self.from_dateEdit.date().toPyDate()
        to_date = self.to_dateEdit.date().toPyDate()
        bool_a = self.avail_check.isChecked()

        self.controller = PRV_Controller.Controller(from_date, to_date)
        self.table_data = self.controller.get_tableData(from_date, to_date, bool_a)


        self.model = PRV_TableModel.TableModel(self.table_data, self.header, from_date, to_date)
        #self.model.returnChecked()
        self.table.setModel(self.model)
        self.table.setMinimumWidth(1850)
        self.table.setMinimumHeight(730)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True) 
        header.setSectionResizeMode(QHeaderView.Stretch) 
        delegate = PButtonDelegate.PushButtonDelegate(self.table)
        self.table.setItemDelegateForColumn(1, delegate)
        delegate.clicked.connect(self.on_clickPname)


        self.add_participant_button = QPushButton('Add Participant', self)
        self.add_participant_button.setFixedWidth(300)
        self.add_participant_button.clicked.connect(self.launch_popup)
        self.grid.addWidget(self.add_participant_button, 5, 2)
        
        self.ex_participant_button = QPushButton('Export Participant', self)
        self.ex_participant_button.setFixedWidth(300)
        self.ex_participant_button.clicked.connect(partial(self.onclick_export,self.model))
        self.grid.addWidget(self.ex_participant_button, 5, 3)

        self.display_button.clicked.connect(partial(self.onclick_display))

        
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.show()

    def on_clickPname(self, index):
        pid = self.sender().text[index.row()]
        self.panel = ParticipantDetailsView.PrettyWidget(int(pid))
        return


    def slider_valuechange(self,value):
        self.rep_value_label.setText(str(value))

    def launch_popup(self):
        pop_up = PRV_InputDialog.InputDialog(self)
        pop_up.show()
        button = pop_up.exec()
        if button == 1:
            #print('kkk')
            a,b = pop_up.getInputs()
            print(a)
        else:
            print(button)

        #a,b = pop_up.getInputs()
        #print('a')

    def selectionchange_fed(self, x ,i):
        return

    def onclick_display(self):
        #data = self.dao.get_data2()
        from_date = self.from_dateEdit.date().toPyDate()
        to_date = self.to_dateEdit.date().toPyDate()
        data_rep = self.controller.get_rep(from_date, to_date)
        bool_a = self.avail_check.isChecked()
        #avail_arr = self.dao.get_pAvail()
        data_rep_avail = self.controller.get_avail(data_rep,bool_a)
        data_rep_avail = self.controller.format_data(data_rep_avail)
        #print(data_rep_avail)
        data_rep_avail.sort(key=lambda x: x[1], reverse=True)

        self.temp_arr = []
        fed_selected = int(self.fed_cb.currentData())
        perf_value = int(self.rep_value_label.text())
        for participant in data_rep_avail:
            if(fed_selected==-1 or self.feds[fed_selected] in participant[2]):
                if participant[1] >= int(self.rep_value_label.text()):
                    self.temp_arr.append(participant)
        if(self.temp_arr!=[]):
            self.model.update(self.temp_arr, from_date, to_date)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No data")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()    
        #self.model = TableModel(self.temp_arr, self.header)
        #self.table.setModel(self.model)

    def onclick_export(self,model):
        data,notAvail = model.getCheckedData()
        np_arr= np.asarray(data)

        if not model.checkChecked():
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("No participant selected")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        else:
            if notAvail:

                msg = QMessageBox()
                msg.setWindowTitle("Participant Unavailable")
                msg.setText("Do you want export unavailable participant(s)?")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                msg.setIcon(QMessageBox.Question)
                button = msg.exec()
                if button == QMessageBox.Yes:
                    print("Yes!")
                    try:
                        with open("jj.csv", 'w', newline='') as csvfile:
                            writer = csv.writer(csvfile, delimiter=',')
                            writer.writerows(np_arr)
                            msg = QMessageBox()
                            msg.setWindowTitle("Success")
                            msg.setText("Participant(s) exported")
                            #msg.setIcon(QMessageBox.Critical)
                            msg.exec_()
                    except PermissionError:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("Please close csv file")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                else:
                    print("No!")
                    #self.msg.buttonClicked.connect(self.popup_button)
                    msg = QMessageBox()
                    msg.setWindowTitle("Export Abort")
                    msg.setText("Export aborted")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

            else:
                try:
                    with open("jj.csv", 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerows(np_arr)
                        msg = QMessageBox()
                        msg.setWindowTitle("Success")
                        msg.setText("Participant(s) exported")
                        #msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                except PermissionError:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText("Please close csv file")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        returnInputDialog


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    GUI = PrettyWidget()
    GUI.showMaximized()
    sys.exit(app.exec_())

#set layout width
#https://stackoverflow.com/questions/19815061/pyside-set-width-of-qvboxlayout/19816024

#QDialog
#https://stackoverflow.com/questions/56019273/how-can-i-get-more-input-text-in-pyqt5-inputdialog
#https://www.youtube.com/watch?v=_NRwGaiv4RQ

#checkbox in table
#https://www.programmersought.com/article/27755841141/
#https://www.programmersought.com/article/19195841305/

#export data to csv
#https://stackoverflow.com/questions/50459119/writing-a-3d-numpy-array-to-a-csv-file/52145217

#find last element in list
#https://stackoverflow.com/questions/1630320/what-is-the-pythonic-way-to-detect-the-last-element-in-a-for-loop

#checkbox
#https://pythonprogramminglanguage.com/pyqt-checkbox/

#update table data
#https://stackoverflow.com/questions/8983769/how-to-update-qabstracttablemodel-and-qtableview-after-sorting-the-data-source

#search in 2d array
#https://stackoverflow.com/questions/12807079/how-to-determined-if-a-2-dimensional-list-contain-a-value

#try catch csv writing
#https://stackoverflow.com/questions/44553093/how-to-write-to-csv-in-python-with-exceptions-in-the-middle