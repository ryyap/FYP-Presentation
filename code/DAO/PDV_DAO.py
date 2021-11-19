import os
import pandas as pd
import pickle
from collections import OrderedDict
import re
import math

class DAO():
    def __init__(self):
        filepath = "..\\SV_DB\\dbs_v2.pkl"
        file = open( filepath, "rb")
        self.pdata = pickle.load(file)

    def get_fid_and_fpid(self, pid):
        df = self.pdata['fpid_to_pid']
        data = df[(df['pid'] == pid) & (df['rid'] == 0)]
        #print(data)
        df = data[['fid', 'fpid']]
        #arr = data[['fid', 'fpid']]
        #print(arr)
        return(df)


    def get_fed_overall_data(self, fed):
        arr = []
        df = self.pdata['fed_round_info']
        data = df[(df['fid'] == fed)]
        #acc = data['acc']
        data['date'] = pd.to_datetime(data['time']).dt.strftime('%d/%m/%Y')
        #.astype(str)
        return data

    def get_fedtopic_fid(self):
        df = self.pdata['fedtopic_fid']
        return df

    def get_contribution(self, fed, fpid):
        #print('k')
        arr = []
        df = self.pdata['p_participate']
        data = df[(df['fid'] == fed)]
        rounds = data['rid'].unique()
        #print(data)

        for x in rounds:
            total_pos = 0
            total_neg = 0
            temp = data[data['rid'] == x]
            contribution_arr = temp['fullset contribution'].values
            con_data = temp[(temp['fpid']==fpid)]
            con_data = con_data['fullset contribution'].values[0].item()

            for item in contribution_arr:
                if item >= 0:
                    total_pos = total_pos + item
                else:
                    total_neg = total_neg + item

            if total_pos > abs(total_neg):
                    conp_data = con_data/total_pos * 100
            else:
                
                    conp_data = con_data/total_neg * 100
            arr.append([con_data,conp_data.item()])

        #print(type(arr[0][0]))
        #print(rounds)
        return arr, rounds