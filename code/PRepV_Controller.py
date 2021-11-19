from functools import partial
import numpy as np
import math
import pandas as pd
from datetime import datetime
import os
import pickle

from DAO import PRepV_DAO

class Controller():
    def __init__(self, from_date, to_date, fed_arr):
        dao = PRepV_DAO.DAO()
        self.raw_data = dao.get_data()
        self.fed_arr = fed_arr
        self.from_date = from_date
        self.to_date = to_date

    def get_fdata(self):
        fdata = []
        for x in range(len(self.raw_data)):
            temp =  self.format_data(self.raw_data[x], self.fed_arr[x]+' Overall', self.from_date, self.to_date)
            fdata.append(temp)
        return fdata

    def get_overallData(self,fdata):
        arr =[]
        for topic in fdata:
            temp = []
            #first = True
            #print(topic)
            for x in range(3,5):

                if x==3:
                    for y in range(len(topic[x])):
                        temp.append(topic[x][y])
                        #print(topic[x][y])
                else:
                    if len(topic[1]) == 10:
                        for y in range(len(topic[x])):
                            temp[y] += topic[x][y]
                            #print(topic[x][y])
            arr.append(temp)

        overall_data = ['Overall',
                             ['104', '108', '107', '105', '103', '110', '109', '102', '106', '101'],
                             ['NLP', 'CV', 'IR'],
                             arr[0],
                             arr[1],
                             #arr[2]
                            ]
        #print(overall_data)
        return overall_data

    def format_data(self, data, fed, fDate, tDate, perf=10):
        from_date = fDate
        to_date = tDate
        if(data[0][0][1]== data[1][0][1]):
            temp_arr = data[0][0][1]
        else:
            temp_arr = data[0][0][1] + data[1][0][1]
        arr = [fed,
               temp_arr,
               [data[0][0][0], data[1][0][0], ],
              ]

        for fed in data:
            #temp_arr = []
            rep_arr = []
            first = True
            for monthly_data in fed:
                #print(monthly_data)
                #print("monthly")
                date = datetime.strptime(monthly_data[4], '%d/%m/%Y').date()
                if from_date <= date <= to_date:

                    if monthly_data[3] >= perf:
                        if first:
                            for x in monthly_data[2]:
                                rep_arr.append(x)
                            first = False
                        else:
                            for x in range(len(rep_arr)):
                                #print(x)
                                #print("before")
                                print(rep_arr)
                                rep_arr[x] += monthly_data[2][x]
                                #print("after")
                                #print(rep_arr)
                                pass
                                #print(rep_arr)

                    else:
                        if rep_arr == []:
                            for p in monthly_data[1]:
                                rep_arr.append(0)
                            first = False
                        #print(rep_arr)
                
                else:
                    if rep_arr == []:
                        for p in monthly_data[1]:
                            rep_arr.append(0)
                        first = False

                   
            #print(rep_arr)
            arr.append(rep_arr)

        #print('fed arr')
        print(arr)    
        return arr

