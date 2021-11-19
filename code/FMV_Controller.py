from functools import partial
import numpy as np
import math
import pandas as pd
import os
import pickle
from collections import OrderedDict

from DAO import FMV_DAO

class Controller():
    def __init__(self, fid):
        dao = FMV_DAO.DAO()
        self.data_arr = dao.get_model_data(fid) 
        self.fed_acc, self.fed_loss = dao.get_fed_overall_data(fid)
        self.p_contribution = dao.get_contribution(fid)

    def get_top10(self):

        #print(data_arr[9])

        top10_arr = []
        

        for item in self.data_arr:
            ordered_dict = OrderedDict(sorted(item.items(), key=lambda t: t[1], reverse=True)[:10])
            p_arr = []
            acc_arr = []
       
            for items in ordered_dict.items():
                p_arr.append(items[0].split(' '))
                acc_arr.append(items[1])
                
            top10_arr.append([p_arr,acc_arr])

        return top10_arr

    def get_participants(self):
        arr = []
        for items in self.data_arr[0].items():
            if (not (' ' in items[0]) and items[0] != ''):
                arr.append(items[0])
        #print(arr)
        return arr

    def get_fullmodel_data(self, participants):
        #print(data)
        fed_data = []
        fed_pos = []
        
        for dictionary in self.data_arr:
            ordered_dict = OrderedDict(sorted(dictionary.items(), key=lambda t: t[1], reverse=True))
            #print(dictionary.keys())
            i = 1
            for item in ordered_dict.items():
                 #print(item)
                 p = item[0].split(' ')
                 if len(p) == len(participants):
                    #print(p)
                    #print(item[1])
                    #print(i)
                    fed_data.append(item[1])
                    fed_pos.append(i)
                 i = i+1
        #print(fed_data)
        return fed_data, fed_pos


    def get_marginal_gain_arr(self, data):
        arr = []
        for x in range(len(data)):
            if (x == 0):
                arr.append(float(data[0]))
            else:
                y = float(data[x])
                #x = x - 1
                y = y - float(data[x-1])
                arr.append(float(format(y, '.4f')))
        #print(arr)
        return arr

    def get_top20_acc(self):
        file_participants_acc = []
        
        for item in self.data_arr:
            ordered_dict = OrderedDict(sorted(item.items(), key=lambda t: t[1], reverse=True)[:20])
            p_arr = []
            acc_arr = []
            for items in ordered_dict.items():
                p_arr.append(items[0].split(' '))
                acc_arr.append(items[1])
        
            file_participants_acc.append([p_arr,acc_arr])    
        return file_participants_acc

    def format_data(self, data):
        
        round_arr = []
        
        for item in data:
            arr = []
            for x in range(0,len(item[1]),5):
                temp = []
                for y in range(5):
                    temp.append(int(item[1][x+y]*1000))
                arr.append(temp)
            round_arr.append(arr)
        return round_arr

    def add_fullmodel_top10(self, top10_arr, participants, fullmodel_arr):
        for x in range(len(top10_arr)):
            exist = False
            for arr in top10_arr[x][0]:

                if len(arr) == len(participants):
                    exist = True
                    break
                    
            if(exist == False):
                top10_arr[x][0].append(participants)
                top10_arr[x][1].append(fullmodel_arr[x])

    def get_numRound(self):
        return len(self.data_arr)