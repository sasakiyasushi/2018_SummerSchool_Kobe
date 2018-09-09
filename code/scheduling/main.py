# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:48:21 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os
import datetime

##時間計測
t1 = time.time()

##外部ファイルインポート
from CONSTANTS import RES_COL
from CSV_DATA import id_arr, category_arr
from MyClass import Schedule


###################################
###  テスト用（上限人数設定）
#n = 1000
#id_arr = id_arr[:n]
#category_arr = category_arr[:n]

###################################


##シミュレーションを行う関数
def simulation(ID, category):
    s = Schedule(ID, category)
    s.make_schedule()
    s.insert_trip()
    return s.to_list()

##シミュレーションを実行し，結果を一つのリストに格納
result = [x for inner_list in map(simulation, id_arr, category_arr) for x in inner_list]

df_res = pd.DataFrame(result, columns=RES_COL)



##出力パスの設定
os.chdir(r"..\..\data\result")

##現在時刻でファイル名の作成
now = datetime.datetime.now()
file_name = r"res_{0:%Y%m%d%H%M%S}.csv".format(now)

##出力
df_res.to_csv(file_name, index=False)


##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")


