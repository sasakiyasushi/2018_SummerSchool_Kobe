# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:11:17 2018

@author: nakano
"""

import os
import csv
import pandas as pd
import setting_summer

os.chdir(r"E:/夏の学校2018/model2018/model2018/Japanese/配布データ/PTデータ")

"""
df1・・・生データフレーム,
df2・・・目的別を整理・縮約したデータフレーム,
df2_person・・・df2からTripChainIDの重複を削除したデータフレーム,
df3・・・df2からStaytimeをTripChainIDごとに合計し，Total Stay Timeを算出したデータフレーム
"""

#df1 = pd.read_csv("PTdata1.csv",encoding="SHIFT-JIS")
df2 = pd.read_csv("PTdata2.csv",encoding="SHIFT-JIS")
#df3 = pd.read_csv("PTdata3.csv",encoding="SHIFT-JIS")

#ヒストグラム用
Max_Hist = max(df2['TripNumber'].unique().tolist())
Min_Hist = min(df2['TripNumber'].unique().tolist())

#以下__main__
#集計対象を指定
Data = df2
Purpose = "work"
Category = "men"

df2_named = setting_summer.Dataframe(Data,Purpose,Category)
df2_person = df2_named.drop_duplicates(['TripChainID'])

#活動数分布
Hist_activity = []
for i in range(Min_Hist,Max_Hist+1):    
    df_trip = df2_person['TripNumber'] ==i
    aaa = [df_trip.sum()]
    
    Hist_activity.append(aaa)

#出力
file_name = "Hist-AF_"+Purpose+"_"+Category+".csv"

with open(file_name, 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(Hist_activity) # 2次元配列も書き込める