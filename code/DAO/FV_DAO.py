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

    def get_fed_overall_data(self):
        arr = []
        df = self.pdata['fed_round_info']
        df['date'] = pd.to_datetime(df['time']).dt.strftime('%d/%m/%Y')
        df = df[['date', 'fid', 'rid', 'acc', 'loss', 'all participants']]
        #print(datetime)
        return df

    def get_fedtopic_fid(self):
        df = self.pdata['fedtopic_fid']
        return df