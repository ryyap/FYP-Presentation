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
import numpy as np
import math
import pandas as pd
from collections import OrderedDict
import re

import FMV_Controller


class PrettyWidget(QMainWindow):
    def __init__(self, fid=5):
        super(PrettyWidget, self).__init__()
        self.initUI(fid)

    def initUI(self, fid):

        # self.setGeometry(100, 100, 800, 600)
        #print('a')
        self.setWindowState(Qt.WindowMaximized)
        self.center()
        self.setWindowTitle('Model')

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.grid = QGridLayout()
        self.widget.setLayout(self.grid)

        #self.filepath_arr = []
        
        self.participants_acc_arr = []
        self.participant_arr = []
        
        self.marginal_gain_arr = []
        self.top20 = []
        self.formatted_top20 = []
        self.rounds = []
        self.cur_round = 0
        self.fullmodel_pos = []

        data_arr = []
        fullmodel_data_arr = []

        self.controller = FMV_Controller.Controller(fid)
        self.participants_acc_arr = self.controller.get_top10()
        self.participant_arr = self.controller.get_participants()
        fullmodel_data_arr, self.fullmodel_pos = self.controller.get_fullmodel_data(self.participant_arr)
        self.marginal_gain_arr = self.controller.get_marginal_gain_arr(fullmodel_data_arr)
        self.top20 = self.controller.get_top20_acc()
        self.formatted_top20 = self.controller.format_data(self.top20)
        self.controller.add_fullmodel_top10(self.participants_acc_arr, self.participant_arr, fullmodel_data_arr)
        fed_acc = self.controller.fed_acc
        fed_loss = self.controller.fed_loss
        self.p_contribution = self.controller.p_contribution
        rounds = self.controller.get_numRound()

        for x in range(rounds):
            self.rounds.append(x+1)

        self.cur_round = self.rounds[-1]-1

        self.ind_lbl = QLabel("Model: {}".format(fid), self)
        self.ind_lbl.setStyleSheet("QLabel{font-size: 18pt;}")
        self.grid.addWidget(self.ind_lbl, 0, 0, 1, 3)    

        self.figure1 = matplotlib.figure.Figure(figsize=(18.5, 4))
        self.canvas1 = FigureCanvas(self.figure1)
        self.plot1( fed_acc, fed_loss, self.p_contribution[self.rounds[-1]-1], self.participant_arr, self.rounds)
        self.figure1.tight_layout()
        self.grid.addWidget(self.canvas1, 1, 0, 1, 3)

        intermediateWidget_model_participants = QWidget(self.widget)
        intermediateWidget_model_participants.setStyleSheet("border: 1px solid black;")
        self.grid.addWidget(intermediateWidget_model_participants, 2, 0)
        self.model_instruction_vbox = QVBoxLayout()
        self.grid.addLayout(self.model_instruction_vbox,2,0)
        self.model_instruction_title_label = QLabel("View Round Data")
        self.model_instruction_title_label.setStyleSheet("margin: 10px; font-size: 14pt;")
        self.model_instruction_label = QLabel("Each marker on the Marginal Gain Per Round graph represents"+
            "\nthe accuracy of each round. Click on a marker to display details"+
            "\nof the top 10 and full model of the selected round.")
        self.model_instruction_label.setStyleSheet("margin: 10px; font-size: 10pt;")
        self.model_instruction_vbox.addWidget(self.model_instruction_title_label)
        self.model_instruction_vbox.addWidget(self.model_instruction_label)
        self.model_instruction_vbox.setAlignment(Qt.AlignTop)

        self.figure2 = matplotlib.figure.Figure(figsize=(4, 4))
        self.canvas2 = FigureCanvas(self.figure2)
        self.plot2(self.marginal_gain_arr, self.rounds)
        self.canvas2.mpl_connect('button_press_event', self.onclick)
        self.grid.addWidget(self.canvas2, 2, 1)

        self.figure3 = matplotlib.figure.Figure(figsize=(4, 4))
        self.canvas3 = FigureCanvas(self.figure3)
        self.plot3(self.cur_round+1, self.p_contribution[self.cur_round])
        self.grid.addWidget(self.canvas3, 2, 2)

        self.figure4 = matplotlib.figure.Figure(figsize=(4, 4))
        self.canvas4 = FigureCanvas(self.figure4)
        self.plot4(self.participants_acc_arr[self.cur_round], self.fullmodel_pos[self.cur_round], len(self.participant_arr))
        self.grid.addWidget(self.canvas4, 3, 0)

        
        intermediateWidget_model_participants = QWidget(self.widget)
        intermediateWidget_model_participants.setStyleSheet("border: 1px solid black;")
        self.grid.addWidget(intermediateWidget_model_participants, 3, 1)
        self.model_participants_vbox = QVBoxLayout()
        self.grid.addLayout(self.model_participants_vbox,3,1)
        self.model_tittle_label = QLabel("Participants in Top 10 + Full Model")
        self.model_tittle_label.setStyleSheet("margin: 10px; font-size: 14pt;")
        self.model_label = QLabel("")
        self.model_label.setStyleSheet("margin: 10px; font-size: 12pt;")
        self.add_participant_to_label(self.model_label, self.participants_acc_arr[self.cur_round][0], self.fullmodel_pos[self.cur_round])
        self.model_participants_vbox.addWidget(self.model_tittle_label)
        self.model_participants_vbox.addWidget(self.model_label)
        self.model_participants_vbox.setAlignment(Qt.AlignTop)
        

        intermediateWidget_submodel_instruction = QWidget(self.widget)
        intermediateWidget_submodel_instruction.setStyleSheet("border: 1px solid black;")
        self.grid.addWidget(intermediateWidget_submodel_instruction, 4, 0)
        self.submodel_instruction_vbox = QVBoxLayout()
        self.grid.addLayout(self.submodel_instruction_vbox,4,0)
        self.submodel_instruction_title_label = QLabel("View Submodel Data")
        self.submodel_instruction_title_label.setStyleSheet("margin: 10px; font-size: 14pt;")
        self.submodel_instruction_label = QLabel("Each square in Top 20 Model in Round X graph represents"+
            "\na submodel accuracy. Click on the square to see display"+
            "\nsubmodel details.")
        self.submodel_instruction_label.setStyleSheet("margin: 10px; font-size: 10pt;")
        self.submodel_instruction_vbox.addWidget(self.submodel_instruction_title_label)
        self.submodel_instruction_vbox.addWidget(self.submodel_instruction_label)
        self.submodel_instruction_vbox.setAlignment(Qt.AlignTop)
        

        self.figure5 = matplotlib.figure.Figure(figsize=(4, 4))
        self.canvas5 = FigureCanvas(self.figure5)
        self.plot5(self.formatted_top20[self.cur_round])
        self.canvas5.mpl_connect('button_press_event', self.onclick2)
        self.grid.addWidget(self.canvas5, 4, 1)

        intermediateWidget_submodel = QWidget(self.widget)
        intermediateWidget_submodel.setStyleSheet("border: 1px solid black;")
        self.grid.addWidget(intermediateWidget_submodel, 4, 2)
        self.submodel_vbox = QVBoxLayout()
        self.grid.addLayout(self.submodel_vbox,4,2)
        self.submodel_tittle_label = QLabel("Sub Model Details")
        self.submodel_tittle_label.setStyleSheet("margin: 10px; font-size: 14pt;")
        self.submodel_label = QLabel("")
        self.submodel_label.setStyleSheet("margin: 10px; font-size: 12pt;")
        self.add_submodel_to_label(self.submodel_label, self.top20[self.cur_round], 0)
        self.submodel_vbox.addWidget(self.submodel_tittle_label)
        self.submodel_vbox.addWidget(self.submodel_label)
        self.submodel_vbox.setAlignment(Qt.AlignTop)
        

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        

        self.show()

    def onclick(self, event):
        # print('xdata=%f' %(event.xdata))
        x1 = event.xdata
        x2 = 0
        # print('x1: ', x1)
        if isinstance(x1, float):
            if x1 > 0:
                x2 = round(x1)
                x2 = int(x2)
                print ('x2: ',x2)

        y1 = event.xdata
        y2 = 0
        # print('x1: ', x1)
        if isinstance(y1, float):
            if y1 > 0:
                y2 = round(y1)
                y2 = int(y2)
                # print ('x2: ',x2)

        # print(self.get_participant_contribution(x))
        self.cur_round = x2-1
        #print("curr round: ", self.cur_round)
        self.ax5.cla()
        self.plot3(x2 , self.p_contribution[self.cur_round])
        self.ax6.cla()
        self.plot4(self.participants_acc_arr[self.cur_round],self.fullmodel_pos[self.cur_round],len(self.participant_arr))
        self.ax7.cla()
        self.plot5(self.formatted_top20[self.cur_round])
        self.add_participant_to_label(self.model_label, self.participants_acc_arr[self.cur_round][0], self.fullmodel_pos[self.cur_round])
        self.add_submodel_to_label(self.submodel_label, self.top20[self.cur_round], 0)

        # self.canvas2.draw_idle()
        return

    def onclick2(self, event):
    
        x1 = event.xdata
        x2 = 0
        # print('x1: ', x1)
        if isinstance(x1, float):
            if x1 > 0:
                x2 = round(x1)
                x2 = int(x2)
        #print('x2: ',x2)
        # print('x2: ', type(x2))
        y1 = event.ydata
        y2 = 0
        # print('x1: ', x1)
        if isinstance(y1, float):
            if y1 > 0:
                y2 = round(y1)
                y2 = int(y2)

        num = (y2*5+x2)
        self.add_submodel_to_label(self.submodel_label, self.top20[self.cur_round], num)

        return

    def add_participant_to_label(self, label, data, fullmodel_pos):

        label.clear()
        o =''
        strr = ""
        pos_arr =['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        pos_arr.append(str(fullmodel_pos)+'th')

        for x in range(len(data)):
            str1 = ''
            first = True
            for ele in data[x]:
                if first:
                    first = False
                    str1 += ele
                else:
                    str1 += ', ' + ele
            
            #strr += ''+ a
            strr += str(pos_arr[x])+': ' + str1 + '\n'
        
        label.setText(strr)

    def add_submodel_to_label(self, label, data, num):
        label.clear()
        p_string = ""
        first = True
        for x in range (len(data[0][num])):
            if(first):
                first = False
                p_string+=data[0][num][x]
            else:
                p_string+=', ' + data[0][num][x]
                           
        #p_string = data[0][num]
        str = "Round : {} \nModel : {}\nDate : \nParticipants : {} \nAccuracy : {}\nComment :".format(self.cur_round+1, num+1, p_string, data[1][num]) 
        label.setText(str)
        return


    def plot1(self, fed_acc, fed_loss, contribution, participants, rounds):
        self.figure1.clf()

        fed_acc = list(np.around(np.array(fed_acc),4))
        fed_loss = list(np.around(np.array(fed_loss),4))
        
        ax1 = self.figure1.add_subplot(131)
        ax1.title.set_text('Accuracy Per Round')
        max_value = max(fed_acc)
        max_value = max_value + max_value*0.1
        min_value = min(fed_acc)
        min_value = min_value - min_value*0.1
        ax1.set_ylim(min_value, max_value)
        ax1.set(xlabel="Rounds", ylabel="Accuracy")
        ax1.plot(rounds, fed_acc)
        # zip joins x and y coordinates in pairs
        for x, y in zip(rounds, fed_acc):
            ax1.annotate(y,  # this is the text
                         (x, y),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center')  # horizontal alignment can be left, right or center

        #roundsX = ['1', '2', '3', '4', '5']
        ax2 = self.figure1.add_subplot(132)
        loss = [90, 70, 40, 30, 20]
        ax2.title.set_text('Loss Per Round')
        max_value = max(fed_loss)
        max_value = max_value + max_value*0.1
        min_value = min(fed_loss)
        min_value = min_value - min_value*0.1
        ax2.set_ylim(min_value, max_value)
        ax2.set(xlabel="Rounds", ylabel="Loss")
        ax2.plot(rounds, fed_loss)
        # zip joins x and y coordinates in pairs
        for x, y in zip(rounds, fed_loss):
            ax2.annotate(y,  # this is the text
                         (x, y),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center')  # horizontal alignment can be left, right or center

        

        self.ax3 = self.figure1.add_subplot(133)

        contribution = contribution.sort_values(by=['fullset contribution'] , ascending=False)
        ind = np.arange(len(contribution['fpid'].values))
        bar_width = 0.5
        
        contribution_arr = contribution['fullset contribution'].values
        total_pos = 0
        total_neg = 0
        contribution_percentage_arr = []

        for item in contribution_arr:
            if item >= 0:
                total_pos = total_pos + item
            else:
                total_neg = total_neg + item

        if total_pos > abs(total_neg):
            for item in contribution_arr:
                temp = item/total_pos * 100
                contribution_percentage_arr.append(temp)
        else:
            for item in contribution_arr:
                temp = item/total_neg * 100
                contribution_percentage_arr.append(temp)

        #print(contribution_percentage_arr)

        max_value = max(contribution_percentage_arr)
        max_value = max_value + max_value*0.005
        min_value = min(contribution_percentage_arr)
        min_value = min_value - min_value*0.005
        self.ax3.set_xlim(min_value,max_value)

        
        #contribution = [40, 30, 20, 10, 70, 5, 30, 33, 44, 68]
        self.ax3.barh( ind, contribution_percentage_arr, height=bar_width)
        self.ax3.set_title('Participant Contribution')
        self.ax3.invert_yaxis()
        self.ax3.set_yticks(ind)
        self.ax3.set_yticklabels(contribution['fpid'].values)
        self.ax3.set_xlabel("Contribution %")
        self.ax3.set_ylabel("Pid")

        self.canvas1.draw_idle()
        return

    def plot2(self, marginal_gain, rounds):
        self.figure2.clf()
        ax4 = self.figure2.add_subplot(111)
        ax4.plot(rounds, marginal_gain, marker='o')
        max_value = max(marginal_gain)
        max_value = max_value + max_value*0.1
        min_value = min(marginal_gain)
        min_value = min_value - min_value*20
        ax4.set_ylim(min_value,max_value)
        ax4.set_ylabel("Marginal Gain")
        ax4.set_xlabel("Rounds")
        ax4.set_title("Marginal Gain Per Round")
        # zip joins x and y coordinates in pairs
        for x, y in zip(rounds, marginal_gain):
            ax4.annotate(y,  # this is the text
                         (x, y),  # this is the point to label
                         textcoords="offset points",  # how to position the text
                         xytext=(0, 10),  # distance from text to points (x,y)
                         ha='center')  # horizontal alignment can be left, right or center
        # ax4.legend()
        self.canvas2.draw_idle()
        return

    def plot3(self, round, data):
        self.figure3.clf()
        self.ax5 = self.figure3.add_subplot(111)

        data = data.sort_values(by=['fullset contribution'] , ascending=False)
        ind = np.arange(len(data['fpid'].values))
        bar_width = 0.5
        
        contribution_arr = data['fullset contribution'].values
        total_pos = 0
        total_neg = 0
        contribution_percentage_arr = []

        for item in contribution_arr:
            if item >= 0:
                total_pos = total_pos + item
            else:
                total_neg = total_neg + item

        if total_pos > abs(total_neg):
            for item in contribution_arr:
                temp = item/total_pos * 100
                contribution_percentage_arr.append(temp)
        else:
            for item in contribution_arr:
                temp = item/total_neg * 100
                contribution_percentage_arr.append(temp)

        #print(contribution_percentage_arr)

        max_value = max(contribution_percentage_arr)
        max_value = max_value + max_value*0.005
        min_value = min(contribution_percentage_arr)
        min_value = min_value - min_value*0.005
        self.ax5.set_xlim(min_value,max_value)

        
        #contribution = [40, 30, 20, 10, 70, 5, 30, 33, 44, 68]
        self.ax5.barh( ind, contribution_percentage_arr, height=bar_width)
        self.ax5.set_title('Participant Contribution')
        self.ax5.invert_yaxis()
        self.ax5.set_yticks(ind)
        self.ax5.set_yticklabels(data['fpid'].values)
        self.ax5.set_xlabel("Contribution %")
        self.ax5.set_ylabel("Pid")

        self.canvas3.draw_idle()
        return

    def plot4(self, data, fed_pos, num_participants):
        self.figure4.clf()
        #model = self.get_model()
        #acc = self.get_accuracy()
        #print(data[0])
        model = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        if(len(data[0])>10):
            model.append(str(fed_pos)+'th')
        for x in range(len(data[0])):
            if len(data[0][x]) == num_participants:
                model[x]+='FM'

        acc = [float(numeric_string) for numeric_string in data[1]]
        #print(data[1])
        self.ax6 = self.figure4.add_subplot(111)
        ind = np.arange(len(model))
        bar_width = 0.2
        max_value = max(data[1])
        max_value = max_value + max_value*0.0005
        min_value = min(data[1])
        min_value = min_value - min_value*0.005
        self.ax6.set_xlim(min_value,max_value)
        #self.ax6.set_xlim(data[1][-1]-0.05,data[1][0])
        self.ax6.invert_yaxis()
        #print(data[1])
        
        self.ax6.barh(ind, acc, height=bar_width)
        self.ax6.set_yticks(ind)
        self.ax6.set_yticklabels(model)
        self.ax6.set_xlabel("Model")
        self.ax6.set_ylabel("Accuracy")
        self.ax6.set_title("Top 10 Model + Full Model in Round " + str(self.cur_round+1))
        self.canvas4.draw_idle()
        # tooltip = mpld3.plugins.PointLabelTooltip(ax6, labels=acc)
        # mpld3.plugins.connect(self.figure4, tooltip)
        return

    def plot5(self, data):
        self.figure5.clf()
        rounds = ['1', '2', '3', '4', '5']
        model = ['1', '2', '3', '4']
        marginal_gain = data
        #marginal_gain = self.get_marginal_gain()
        self.ax7 = self.figure5.add_subplot(111)
        a = self.ax7.imshow(marginal_gain)
        #self.ax7.set_xticks(np.arange(len(rounds)))
        #self.ax7.set_yticks(np.arange(len(model)))
        self.ax7.get_xaxis().set_visible(False)
        self.ax7.get_yaxis().set_visible(False)


        # Loop over data dimensions and create text annotations.
        
        for i in range(len(model)):
            for j in range(len(rounds)):
                #print(i, j)
                text = self.ax7.text(j, i, marginal_gain[i][j],
                               ha="center", va="center", color="w")
                #ax7.text.setToolTip("This is a text")
        
        self.ax7.set_title("Top 20 Model in Round {}".format(self.cur_round+1))
        self.canvas5.draw_idle()
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

# command not found (linx/mac error)
# https://stackoverflow.com/questions/22275350/xx-py-line-1-import-command-not-found

#pass data
#https://forum.qt.io/topic/112315/pyqt-pass-data-between-windows-and-run-script-in-second-window/7

#line graph markers
#https://stackoverflow.com/questions/8409095/set-markers-for-individual-points-on-a-line-in-matplotlib

#zip sort unzip
#https://stackoverflow.com/questions/11601961/sorting-multiple-lists-based-on-a-single-list-in-python
