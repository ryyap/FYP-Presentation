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

import ParticipantRecommendationsView
import PRepV_Controller


class PrettyWidget(QMainWindow):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):

        #self.setGeometry(100, 100, 800, 600)
        # self.center()
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('Reputation')

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        # self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)
        # self.vbox.addLayout(self.grid)

        self.rep_lbl = QLabel("Reputation", self)
        self.rep_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        self.grid.addWidget(self.rep_lbl, 0, 0)

        self.prec_button = QPushButton('View Participant Recomendations', self)
        self.prec_button.clicked.connect(self.onclick_openPrec)
        self.prec_button.setFixedWidth(300)
        self.grid.addWidget(self.prec_button, 0, 3, 1, 1)

        self.overall_grid = QGridLayout()
        self.grid.addLayout(self.overall_grid, 1, 0, 1, 4)

        self.widget1 = QWidget(self.widget)
        self.hbox1 = QHBoxLayout()
        self.widget1.setLayout(self.hbox1)
        self.widget1.setFixedWidth(400)
        self.grid.addWidget(self.widget1, 2, 0, 1, 1)

        self.widget2 = QWidget(self.widget)
        self.hbox2 = QHBoxLayout()
        self.widget2.setLayout(self.hbox2)
        self.widget2.setFixedWidth(400)
        self.grid.addWidget(self.widget2, 2, 1, 1, 1)

        self.widget3 = QWidget(self.widget)
        self.hbox3 = QHBoxLayout()
        self.widget3.setLayout(self.hbox3)
        self.widget3.setFixedWidth(850)
        self.grid.addWidget(self.widget3, 2, 2, 1, 2)

        self.widget4 = QWidget(self.widget)
        self.hbox4 = QHBoxLayout()
        self.widget4.setLayout(self.hbox4)
        self.widget4.setFixedWidth(500)
        self.grid.addWidget(self.widget4, 3, 0, 1, 1)

        self.widget5 = QWidget(self.widget)
        self.hbox5 = QHBoxLayout()
        self.widget5.setLayout(self.hbox5)
        self.widget5.setFixedWidth(250)
        self.grid.addWidget(self.widget5, 3, 1, 1, 2)

        self.widget6 = QWidget(self.widget)
        self.hbox6 = QHBoxLayout()
        self.widget6.setLayout(self.hbox6)
        self.widget6.setFixedWidth(800)
        self.grid.addWidget(self.widget6, 3, 2, 1, 2)

        self.fed_grid = QGridLayout()
        self.grid.addLayout(self.fed_grid, 5, 0, 1, 4)

        #data = self.get_data()
        self.fig_canvas_overall = []
        self.fig_canvas_feds = []

        self.from_label = QLabel("Date From:")
        self.from_label.setFixedWidth(100)
        self.from_label.setAlignment(Qt.AlignLeft)
        date = QDate(2021, 7, 1)
        #print(date)
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

        self.pfm_label = QLabel("Performance:")
        self.pfm_label.setFixedWidth(100)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(5)
        self.slider.setFixedWidth(600)
        self.pfm_value_label = QLabel('10', self)
        self.pfm_value_label.setFixedWidth(50)
        self.slider.valueChanged.connect(self.slider_valuechange)
        self.hbox3.addWidget(self.pfm_label)
        self.hbox3.addWidget(self.slider)
        self.hbox3.addWidget(self.pfm_value_label)

        self.fed_label = QLabel('Select Federation: ', self)
        self.fed_label.setAlignment(Qt.AlignLeft)
        self.fed_label.setFixedWidth(150)
        self.fed_cb = QComboBox()
        self.fed_cb.addItem('Overall', -1)
        self.fed_cb.addItem('Natural Language Processing', 0)
        self.fed_cb.addItem('Computer Vision', 1)
        self.fed_cb.addItem('Image Recognition', 2)
        self.fed_cb.setFixedWidth(250)
        self.hbox4.addWidget(self.fed_label)
        self.hbox4.addWidget(self.fed_cb)
   
        self.display_button = QPushButton('Display Selected', self)
        self.display_button.setFixedWidth(300)
        self.display_button.clicked.connect(self.onclick_displaySelected)
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.setFixedWidth(300)
        self.reset_button.clicked.connect(self.onclick_reset)
        self.hbox6.addWidget(self.display_button)
        self.hbox6.addWidget(self.reset_button)

        #self.dao = PRepV_DAO.DAO()
        #raw_data = self.dao.get_data()

        self.fed_arr=['Natural Language Processing', 'Computer Vision', 'Image Recognition']
        
        from_date = self.from_dateEdit.date().toPyDate()
        to_date = self.to_dateEdit.date().toPyDate()
        self.controller = PRepV_Controller.Controller(from_date, to_date, self.fed_arr)
        fdata = self.controller.get_fdata()
        self.overall_data = self.controller.get_overallData(fdata)

        fdata.insert(0,self.overall_data)
        self.plot_loop(fdata, self.overall_grid, self.fig_canvas_overall)
        self.figure = matplotlib.figure.Figure(figsize=(4, 3.6))
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 5, 0, 1, 1)
        self.plot(self.overall_data, self.figure, self.canvas)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.show()

    def plot_loop(self, data, layout, fig_canvas):
        self.clear_plot(fig_canvas)
        #print(data[0])
        #print('run')
        y = 0
        z = 0
        for x in range(len(data)):
            #print(x)

            if z == 4:
                z = 0
                y = y + 1
            if len(data) > len(fig_canvas):
                #print('run')
                figure = matplotlib.figure.Figure(figsize=(4.5, 4))
                canvas = FigureCanvas(figure)
                layout.addWidget(canvas, y, z)
                fig_canvas.append([figure, canvas])
            # print(y)
            # print(z)
            # print(data)
            if x == 0:
                self.plot(data[x], fig_canvas[x][0], fig_canvas[x][1])
            else:
                self.plot(data[x], fig_canvas[x][0], fig_canvas[x][1])
            # self.fig_canvas[x][1].mpl_connect('button_press_event', partial(self.onclick_openFed,'python Federation.py','x'))
            #print(data[x])

            #temp
            #fig_canvas[x][1].mpl_connect('button_press_event', partial(self.onclick_openFed, data[x]))
            z = z + 1
        return

    def onclick_displaySelected(self):
        self.figure.clf()
        self.canvas.draw_idle()
        from_date = self.from_dateEdit.date().toPyDate()
        to_date = self.to_dateEdit.date().toPyDate()
        raw_data = self.controller.raw_data
        fed_select= self.fed_cb.currentData()
        perf = int(self.pfm_value_label.text())
        #print('perf')
        #print(perf)

        ###/////

        fdata=[]

        if(fed_select>=0):
            temp =  self.controller.format_data(raw_data[fed_select], self.fed_arr[fed_select], from_date, to_date, perf)
            #print(temp)
            self.plot(temp, self.figure, self.canvas)
        else:
            fdata=[]
            for x in range(len(raw_data)):
                temp =  self.controller.format_data(raw_data[x], self.fed_arr[x], from_date, to_date, perf)
                #print(temp)
                fdata.append(temp)
            #print(fdata)
            #print(self.fdata)
            #print(fdata)
            arr =[]
            for topic in fdata:
                temp = []
                #first = True
                for x in range(3,5):
                    if x==3:
                        for y in range(len(topic[x])):
                            temp.append(topic[x][y])
                            #print(temp)
                            #print(topic[x][y])
                    else:
                        #print(topic[x])
                        if len(topic[1]) == 10:
                            for y in range(len(topic[x])):
                                temp[y] += topic[x][y]
                                #print(topic[x][y])
                                pass
                #print(temp)
                arr.append(temp)

            data = ['Overall',
                    ['104', '108', '107', '105', '103', '110', '109', '102', '106', '101'],
                    ['NLP', 'CV', 'IR'],
                    arr[0],
                    arr[1],
                    #arr[2]
                   ]

            #fdata.insert(0,self.overall_data)
            #print(fdata)
            if(any(arr[0]) or any(arr[1]) ):
                self.plot(data, self.figure, self.canvas)
                #print(data)
            else:
                msg = QMessageBox()
                msg.setWindowTitle("No Data")
                msg.setText("No data in selected date range")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

        return

    def clear_plot(self, fig_canvas):
        for item in fig_canvas:
            item[0].clf()
            item[1].draw_idle()
            # print(item)
        return

    def onclick_reset(self):
        #self.clear_plot(self.fig_canvas_feds)
        #self.plot_loop2(self.data2, self.fed_grid, self.fig_canvas_feds)
        self.figure.clf()
        self.canvas.draw_idle()
        self.plot(self.overall_data, self.figure, self.canvas)

        date = QDate(2021, 7, 1)
        self.from_dateEdit.setDate(date)
        self.to_dateEdit.setDateTime(QDateTime.currentDateTime())
        self.slider.setValue(0)
        return

    def onclick_openPrec(self):
        self.panel = ParticipantRecommendationsView.PrettyWidget()
        return

    def slider_valuechange(self,value):
        self.pfm_value_label.setText(str(value))

    
    def plot(self, data, fig, canvas):
        fig.clf()
        #print('plot')
        #print(data[3][:10])

        #title = data[0][0] + ' ' + data[0][1]

        if data[0] == 'Overall':
            colorArr = ['red', 'green', 'blue']
        elif 'Natural Language Processing' in data[0]:
            colorArr = ['red', 'firebrick', 'orange']
        elif 'Computer Vision' in data[0]:
             colorArr = ['green', 'darkgreen', 'olive']
        else:
            colorArr = ['blue', 'midnightblue', 'purple']


        title = data[0]
        participant = data[1]
        #print(participant)
        if(len(participant)==10):

            label = data[2]
            d1 = data[3][:10]
            d2 = data[4][:10]
            #d3 = data[5][:10]
            bar = [d1, d2]

            ind = np.arange(len(participant))
            bar_width = 0.2
            bar_padding1 = np.add(d1, d2).tolist()

            ax1 = fig.add_subplot(111)
            ax1.barh(ind, d1, height=bar_width, color=colorArr[0])
            ax1.barh(ind, d2, left=d1, height=bar_width, color=colorArr[1])
            #ax1.barh(ind, d3, left=bar_padding1, height=bar_width, color=colorArr[2])

            fig.gca().invert_yaxis()
            ax1.set_yticks(ind)
            ax1.set_yticklabels(participant)
            ax1.set_ylabel("Participant")
            ax1.set_xlabel("Contribution")
            ax1.set_title(title)
            ax1.legend( [(label[0]), (label[1])], loc = "lower right")

            canvas.draw_idle()
        else:
            participant = data[1][:10]
            label = data[2]
            d1 = data[3][:10]
            ind = np.arange(len(participant))
            bar_width = 0.2
            ax1 = fig.add_subplot(111)
            ax1.barh(ind, d1, height=bar_width, color=colorArr[0])
            fig.gca().invert_yaxis()
            ax1.set_yticks(ind)
            ax1.set_yticklabels(participant)
            ax1.set_ylabel("Participant")
            ax1.set_xlabel("Contribution")
            ax1.set_title(title)
            ax1.legend( [(label[0]), (label[1])], loc = "lower right")

            canvas.draw_idle()
        return

    def plot_overall(self, data, fig, canvas):
        fig.clf()
        #print('plot')
        #print(data[3][:10])

        #title = data[0][0] + ' ' + data[0][1]

        if data[0] == 'Overall':
            colorArr = ['red', 'green', 'blue']
        elif 'Natural Language Processing' in data[0]:
            colorArr = ['red', 'firebrick', 'orange']
        elif 'Computer Vision' in data[0]:
             colorArr = ['green', 'darkgreen', 'olive']
        else:
            colorArr = ['blue', 'midnightblue', 'purple']


        title = data[0]
        participant = data[1][:10]
        label = data[2]
        d1 = data[3][:10]
        d2 = data[4][:10]
        d3 = data[5][:10]
        bar = [d1, d2, d3]

        ind = np.arange(len(participant))
        bar_width = 0.2
        bar_padding1 = np.add(d1, d2).tolist()

        ax1 = fig.add_subplot(111)
        ax1.barh(ind, d1, height=bar_width, color=colorArr[0])
        ax1.barh(ind, d2, left=d1, height=bar_width, color=colorArr[1])
        ax1.barh(ind, d3, left=bar_padding1, height=bar_width, color=colorArr[2])

        fig.gca().invert_yaxis()
        ax1.set_yticks(ind)
        ax1.set_yticklabels(participant)
        ax1.set_ylabel("Participant")
        ax1.set_xlabel("Contribution")
        ax1.set_title(title)
        ax1.legend([(label[0]), (label[1]), (label[2])], loc = "lower right")

        canvas.draw_idle()
        return

    def plot_popup(self, data):

        title = data[0]
        participant = data[1]
        label = data[2]
        d1 = data[3]


        ind = np.arange(len(participant))
        bar_width = 0.2

        plt.barh(ind, d1, height=bar_width)


        plt.gca().invert_yaxis()
        plt.yticks(ind,participant)
        plt.ylabel("Participant")
        plt.xlabel("Contribution")
        plt.title(title)
        #plt.legend([ (label[0], d1), (label[1], d2), (label[2], d3)],loc='lower right')
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

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

# pyqt4 + matplotlib
# https://stackoverflow.com/questions/36086361/embed-matplotlib-in-pyqt-with-multiple-plot

# pyqt4 to pyqt5
# https://stackoverflow.com/questions/45501514/attributeerror-module-pyqt5-qtgui-has-no-attribute-qwidget

# maximize window
# https://www.geeksforgeeks.org/pyqt5-how-to-open-window-in-maximized-format/

# scrollbar
# https://www.mfitzp.com/tutorials/qscrollarea/

# columnspan / rowspan
# https://stackoverflow.com/questions/38325350/how-to-combine-columns-in-a-layout-colspan-feature

# update plot
# https://stackoverflow.com/questions/53258160/update-an-embedded-matplotlib-plot-in-a-pyqt5-gui-with-toolbar

# multi line label
# desc = QLabel("Title: %s\nSummary: %s " % (title.text, desc.text), self)

# textbox
# https://pythonspot.com/pyqt5-textbox-example/

# date picker
# https://stackoverflow.com/questions/21674060/qt-pyqt4-pyside-qdateedit-calendar-popup-falls-off-screen
# https://stackoverflow.com/questions/61449954/pyqt5-datepicker-popup
# https://stackoverflow.com/questions/8049055/pyqt-get-date-from-the-user

# string to datetime
# https://stackoverflow.com/questions/466345/converting-string-into-datetime

# check if date is in between 2 dates
# https://stackoverflow.com/questions/5464410/how-to-tell-if-a-date-is-between-two-other-dates

# open script
# https://stackoverflow.com/questions/26867723/how-to-call-a-python-script-on-button-click-using-pyqt

#sort multi dimenstional array
#https://stackoverflow.com/questions/20099669/sort-multidimensional-array-based-on-2nd-element-of-the-subarray

#color
#https://matplotlib.org/stable/gallery/color/named_colors.html

#colored stacked bar
#https://stackoverflow.com/questions/58292932/how-can-the-colors-in-a-bar-of-a-matplotlib-stacked-bar-chart-be-specified-indiv