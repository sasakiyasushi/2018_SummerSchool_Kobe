# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:26:00 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os

##時間計測
t1 = time.time()

##　パスの設定
os.chdir(r"..\..\data\PDF")

##分類
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

##目的
purpose = list(range(1,7))

C_P = [f"{c}_{p}" for c in category for p in purpose]

for cp in C_P:

    ##活動数の整理
    df_fre = pd.read_csv(f"PDF_Hist-AF_{cp}.csv",usecols=[0])
    df_fre = df_fre.iloc[:-1,:]
    df_fre.index.name = "frequency"
    df_fre.to_csv(rf"..\activity_generation\frequency_{cp}.csv")
    
    ##開始時刻の整理
    df_st = pd.read_csv(f"PDF_AF-ST_{cp}.csv")
    df_st = df_st.iloc[:-1,:-1]
    
    df_st = df_st.div(df_st.sum(axis=1),axis=0)
    df_st.fillna(0,inplace=True)
    df_st.index.name = "frequency"
    df_st.to_csv(rf"..\activity_generation\start_time_{cp}.csv")
    
    ##活動継続時間の整理
    df_dur = pd.read_csv(f"PDF_ST-D_{cp}.csv")
    df_dur = df_dur.iloc[:-1,:-1]
    
    df_dur = df_dur.div(df_dur.sum(axis=1),axis=0)
    df_dur.fillna(0,inplace=True)
    df_dur.index.name = "start_time"
    df_dur.to_csv(rf"..\activity_generation\duration_{cp}.csv")

##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")