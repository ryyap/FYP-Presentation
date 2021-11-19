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

    def get_model_data(self, fed):
        arr = []
        df = self.pdata['sv_info']
        data = df[df['fid'] == fed]
        data = data["sv dict"]
        for item in data:
            item = {re.sub(r"[(),]", "", str(key), flags=re.I): float(value) for key, value in item.items()}
            arr.append(item)
        return arr

    def get_fed_overall_data(self, fed):
        arr = []
        df = self.pdata['fed_round_info']
        data = df[(df['fid'] == fed)]
        loss = data['loss']
        acc = data['acc']
        return acc,loss

    def get_contribution(self, fed):
        arr = []
        df = self.pdata['p_participate']
        data = df[(df['fid'] == fed)]
        rounds = data['rid'].unique()
        for x in rounds:
            temp = data[data['rid'] == x]
            temp = temp[['fpid','fullset contribution']]
            #temp = temp[temp['fullset contribution'] * 100]
            #temp[temp < 0] = 0

            arr.append(temp)
        #print(data)
        return arr