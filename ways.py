# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:34:53 2020

@author: songxy
"""

import pandas as pd
#AU=王长峰 AND FU=71271031
def get_data():
    data_list = pd.read_excel(r"D:\1论文\个性化\data\test.xlsx",
                              encoding='utf8')
    leaders = data_list.leader.values.tolist()
    codes = data_list.code.tolist()
    results = []
    for leader,code in zip(leaders,codes):
        result = "AU={} AND FU={}".format(leader,code)
        results.append(result)
    return results
 
#results = get_data()
#print(results)