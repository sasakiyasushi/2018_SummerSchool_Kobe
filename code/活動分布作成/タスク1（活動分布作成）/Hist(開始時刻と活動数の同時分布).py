# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:11:17 2018

@author: nakano
"""

import os
import csv
import pandas as pd
import datetime
import setting_summer

os.chdir(r"E:/夏の学校2018/model2018/model2018/Japanese/配布データ/PTデータ")

"""
df1・・・生データフレーム,
df2・・・目的別を整理・縮約したデータフレーム,
df2_person・・・df2からTripChainIDの重複を削除したデータフレーム,
df3・・・df2からStaytimeをTripChainIDごとに合計し，Total Stay Timeを算出したデータフレーム
"""

#データ
#df1 = pd.read_csv("PTdata1.csv",encoding="SHIFT-JIS")
df2 = pd.read_csv("PTdata2.csv",encoding="SHIFT-JIS")
#df3 = pd.read_csv("PTdata3.csv",encoding="SHIFT-JIS")

#ヒストグラム用
Max_Hist = max(df2['TripNumber'].unique().tolist())
Min_Hist = min(df2['TripNumber'].unique().tolist())

#0~24時のリストを秒に変換
h24 = []

#30分単位
time =25*2

for i in range(0,time):
    hour = i*3600
    h24.append(hour)
    
#以下__main__
#集計対象を指定
Data = df2
Purpose = "pastime"
Category = "men"

df2_named = setting_summer.Dataframe(Data,Purpose,Category)
df2_person = df2_named.drop_duplicates(['TripChainID'])

Count_activity = []

for i in range(Min_Hist,Max_Hist+1):
    df_stime = df2_named[df2_named['TripNumber'] ==i]
    
    Count_stime = []
    
    for j in range(len(h24)-1):
        s_bool = ((df_stime['Gtime'] >= h24[j]) & (df_stime['Gtime'] < h24[j+1]))
        Count_stime.append(s_bool.sum())

    Count_activity.append(Count_stime)

"""
#確認用
aaa = 0
for i in range(0,len(Count_activity)):
    print(i)
    aaa += sum(Count_activity[i])
    
print(aaa)
"""

file_name = "AF-ST_"+Purpose+"_"+Category+".csv"

with open(file_name, 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(Count_activity) # 2次元配列も書き込める
    