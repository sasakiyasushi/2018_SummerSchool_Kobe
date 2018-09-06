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
import time

##時間計測
t1 = time.time()

os.chdir(r"..\..\..\data")

file_list = os.listdir()
if "Hist" not in file_list:
    os.mkdir(r".\Hist")

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
Time =25*2

for i in range(0,Time):
    hour = i*3600
    h24.append(hour)
    
    
##出力用ディレクトリ
os.chdir(r".\Hist")


#以下__main__
#集計対象を指定
Data = df2

purpose = list(range(1,7))

category = ['all_all',
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

for Purpose in purpose:
    for Category in category:

        df2_named = setting_summer.filter_Dataframe(Data,Purpose,Category)
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
        
        file_name = "AF-ST_"+str(Category)+"_"+str(Purpose)+".csv"
        
        with open(file_name, 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerows(Count_activity) # 2次元配列も書き込める
##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")