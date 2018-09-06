# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:07:04 2018

@author: nakano
"""

import pandas as pd

"""
data = df1,df2
purpose
1．通勤 2．通学 3．帰宅（自宅） 4．買い物 5．娯楽 6．その他
purpose = list(range(1,7))

CATEGORY_LIST
['all_all',
 'all_men',
 'all_women',
 'under20_all',
 'under20_men',
 'under20_women',
 'over70_all',
 'over70_men',
 'over70_women',
 '20to69_all',
 '20to69_men',
 '20to69_women']
"""


def filter_Dataframe(data,purpose,category):
    
    ###目的別
    df = data[data["Purpose"] == purpose]
    
    ###個人別
    if category == "all_all":
        return df
    else:
        ##性別フィルター
        if "women" in category:
            df = df[df["Sex"] == 2]
        elif "men" in category:
            df = df[df["Sex"] == 1]
        ##年齢フィルター
        if "under20" in category:
            df = df[df["Age"] < 4]
        elif "over70" in category:
            df = df[(df["Age"] > 13) & (df["Age"] < 18)]
        elif "20to69" in category:
            df = df[(df["Age"] > 3) & (df["Age"] < 14)]
        return df
    
##テスト用
#import os
#
###　パスの設定
#os.chdir(r"..\..\..\data")
#
#data = pd.read_csv("PTdata3.csv",encoding = "SHIFT-JIS")
#
#purpose = 1
#category = "over70_women"
#df = filter_Dataframe(data,purpose,category)