from functools import partial
import numpy as np
import math
import pandas as pd
from datetime import datetime
import os
import pickle

from DAO import PDV_DAO

class Controller():
    def __init__(self, fpid):
        acc_arr = [] 
        contribute_arr = []
        rounds_arr = []
        self.curr_arr = []
        self.datetime_arr = []
        fid_fpid_arr = []
        self.fid_arr = []
        self.last_round_contr_arr = []
        self.fedtopic_arr = []
        self.selected_date = 0
        self.selected_fedtopic = 0
        self.date_topic_arr = []


        dao = PDV_DAO.DAO()
        #pickle_data = self.get_pickle_data()

        fid_fpid_df = dao.get_fid_and_fpid(fpid)
        print(fid_fpid_df)
        fid_fpid_arr = fid_fpid_df.values.tolist()
        print(fid_fpid_arr)
        #data_df = self.get_fed_overall_data(pickle_data, test_arr[0][0])
        data_df = dao.get_fed_overall_data(fid_fpid_arr[0][0])
        data_df['pid'] = 1
        for x in range(1, len(fid_fpid_arr)):
                #temp_df = self.get_fed_overall_data(pickle_data, test_arr[x][0])
                temp_df = dao.get_fed_overall_data(fid_fpid_arr[x][0])
                temp_df['pid'] = fid_fpid_arr[x][1]
                data_df = pd.concat([data_df, temp_df])
        #print(data_df)
        date_arr = data_df['date'].unique()
        fedtopic_df = dao.get_fedtopic_fid()
        #print(date_arr)
        temp_arr = []
        #temp
        for date in date_arr:
            temp_arr = []
            data_date_df = data_df[(data_df['date']==date)]
            data_date_df = pd.merge(data_date_df, fedtopic_df, on='fid')
            print(data_date_df)
            temp_fedtopics = data_date_df['fedtopic'].unique()
            #print(temp_fedtopics)
            self.fedtopic_arr.append(temp_fedtopics)
            #print('fed topic arr')
            #print(self.fedtopic_arr)
            for fedtopic in temp_fedtopics:
                #print('topic')
                #print(fedtopic)
                temp = data_date_df[(data_date_df['fedtopic']==fedtopic) & (data_date_df['rid']==0)]
                temp = temp[['fid', 'pid']].values.tolist()
                temp_arr.append(temp)

            print(temp_arr)
            self.date_topic_arr.append(temp_arr)
            print(self.date_topic_arr)

            datefed_acc_arr=[]
            datefed_datetime_arr=[]
            datefed_contribute_arr=[]
            datefed_rounds_arr=[]
            
            for fedtopic in self.date_topic_arr[-1]:
                fedtopic_acc_arr=[]
                fedtopic_datetime_arr=[]
                fedtopic_contribute_arr=[]
                fedtopic_rounds_arr=[]
                #print(fedtopic)
                for row in fedtopic:
                    #print(row)
                    #print(data_date_df)
                    df = data_date_df[(data_date_df['fid']==row[0])]
                    temp_acc = df['acc'].values.tolist()
                    #missing apend
                    fedtopic_acc_arr.append(temp_acc)
                    #print(temp_acc)
                    temp_datetime_arr = df['date'].values.tolist()
                    fedtopic_datetime_arr.append(temp_datetime_arr)
                    #missing append
                    #print(temp_datetime_arr)
                    fed_contribution, fed_rounds = dao.get_contribution(row[0], row[1])
                    #print(fed_contribution)
                    fedtopic_contribute_arr.append(fed_contribution)
                    fedtopic_rounds_arr.append(fed_rounds)
                    #print(fedtopic_contribute_arr)

                datefed_acc_arr.append(fedtopic_acc_arr)
                datefed_datetime_arr.append(fedtopic_datetime_arr)
                datefed_contribute_arr.append(fedtopic_contribute_arr)
                datefed_rounds_arr.append(fedtopic_rounds_arr)

            acc_arr.append(datefed_acc_arr)
            self.datetime_arr.append(datefed_datetime_arr)
            contribute_arr.append(datefed_contribute_arr)
            rounds_arr.append(datefed_rounds_arr)
            #print(acc_arr)

            #print(temp_arr)

            temp_fid_arr = []
            for fedtopic in self.date_topic_arr[-1]:
                temp = []
                for item in fedtopic:
                    #print(item)
                    temp.append(item[0])
                temp_fid_arr.append(temp)
            self.fid_arr.append(temp_fid_arr)
            #print(fid_arr)
            
            temp_last_round_contr_arr = []
            for fedtopic in datefed_contribute_arr:
                temp = []
                for item in fedtopic:
                    temp.append(item[-1][1])
                temp_last_round_contr_arr.append(temp)
            self.last_round_contr_arr.append(temp_last_round_contr_arr)
            #print(last_round_contr_arr)

            temp_curr = []
            for fedtopic in range(len(self.date_topic_arr[-1])):
                #print(fedtopic)
                temp = []
                count= 0
                for curr_fed in range(len(self.date_topic_arr[-1][fedtopic])):
                    #print(curr_fed)
                    fid = self.date_topic_arr[-1][fedtopic][curr_fed][0]
                    #print('fid')
                    #print(fid)

                    for curr_round in range(len(datefed_rounds_arr[fedtopic][curr_fed])):
                    

                        temp.append([datefed_datetime_arr[fedtopic][curr_fed][curr_round], fid, 
                            datefed_rounds_arr[fedtopic][curr_fed][curr_round].item(), 
                            datefed_acc_arr[fedtopic][curr_fed][curr_round], 
                            datefed_contribute_arr[fedtopic][curr_fed][curr_round][0], 
                            datefed_contribute_arr[fedtopic][curr_fed][curr_round][1]])
                    
                        #temp.append(rounds_arr[fedtopic][curr_fed][curr_round].item())
                temp_curr.append(temp)
            self.curr_arr.append(temp_curr)

    def format_data(self,data):
      f_data = []
      for fed in data:
              for x in range(len(fed)):
                #print(fed[x])
                f_data.append(fed[x])
      return f_data