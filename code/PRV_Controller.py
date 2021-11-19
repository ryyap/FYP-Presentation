from functools import partial
import numpy as np
import math
import pandas as pd
from datetime import datetime
import os
import pickle

from DAO import PRV_DAO

class Controller():
    def __init__(self, from_date, to_date):
        self.dao = PRV_DAO.DAO()       

        self.data = self.dao.get_data()
        #self.data_rep = self.get_rep(from_date, to_date)
        self.avail_arr = self.dao.get_pAvail()
        

    def get_tableData(self,from_date, to_date, bool_a):
        data_rep = self.get_rep(from_date, to_date)
        table_data = self.get_avail(data_rep, bool_a)
        table_data = self.format_data(table_data)
        table_data.sort(key=lambda x: x[1], reverse=True)
        return table_data
        

    def get_rep(self, startDate, endDate):

        arr = []

        for participant in self.data:
            rep = 0
            for row in participant:
                date = datetime.strptime(row[3], '%d/%m/%Y').date()
                #print((startDate <= date <= endDate))
                if startDate <= date <= endDate:
                    #arr.append(participant)
                    rep = rep + row[1]
            arr.append([row[0],rep,row[2]])

        #print(arr)
        return arr

    def get_avail(self, data, bool_avail):
        #print(data[0])
        #print(avail_arr[0][1])
        temp_arr = []
        if(not bool_avail):
            for x in range(len(self.avail_arr)):
                temp = data[x]
                temp.append(self.avail_arr[x][1])
                temp_arr.append(temp)
        else:
            for x in range(len(self.avail_arr)):
                if(self.avail_arr[x][1]=='Yes'):
                    temp = data[x]
                    temp.append(self.avail_arr[x][1])
                    print(temp)
                    temp_arr.append(temp)

        #    for x in data:
        #print(temp_arr)
        return temp_arr

    def format_data(self, data):
        #print(data[0])
        temp_data = data
        for row in temp_data:
                fed_str = ''
                first = True
                for fed in row[2]:
                    if first:
                        first = False
                        fed_str = fed_str + fed
                    else:
                        fed_str = fed_str + ', ' + fed 
                        #print(fed_str)
                row[2] = fed_str
        #print(temp_data[0])
        #print('a')
        return temp_data