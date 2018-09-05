# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 08:48:17 2018

@author: sasaki

交通手段選択関数
mode_choice

引数
O : 起点ID
D : 終点ID

"""

import pandas as pd
import numpy as np
import os

##　パスの設定
os.chdir(r"..\..\data\choice")

##データの読み込み
df_time = pd.read_csv("travel_time.csv", encoding="SHIFT-JIS",index_col=[0,1])
df_mode_para = pd.read_csv("para_mode.csv", encoding="SHIFT-JIS",index_col=[0])

##交通手段一覧
mode_list = ["car","train","bus","cycle","walk"]

##旅行時間を辞書に格納
travel_time_dict = df_time.T.to_dict(orient="list")

##目的別のパラメータを辞書に格納(速度向上のため)
mode_para = df_mode_para.iloc[:,0].to_dict()


##効用関数(実際の推定結果に合わせて変更予定)
def mode_utility_function(O, D):
    tmp_tt = travel_time_dict[(O,D)]
    V = np.array([
            mode_para["B_time"] * tmp_tt[0] + mode_para["C_car"],
            mode_para["B_time"] * tmp_tt[1] + mode_para["C_train"],
            mode_para["B_time"] * tmp_tt[2] + mode_para["C_bus"],
            mode_para["B_time"] * tmp_tt[3] + mode_para["C_cycle"],
            mode_para["B_time"] * tmp_tt[4] ##徒歩（定数項なし）
            ])
    return V

##選択確率の計算
def mode_selection_probability(O,D):
    ##効用配列
    V = mode_utility_function(O,D)
    return np.exp(V) / np.exp(V).sum(axis=0)


##交通手段選択関数(選択個数をnで指定)
def mode_choice(O,D,n=1):
    ##重み付き復元抽出
    mode_index = list(range(5))
    result = np.random.choice(mode_index,n,p=mode_selection_probability(O,D))[0]
    return mode_list[result], travel_time_dict[(O,D)][result]


##検証用
import time
import collections
import matplotlib.pyplot as plt
t1 = time.time()
O = 1
D = 10
res_mode, res_tt = zip(*[mode_choice(O,D) for x in range(1000)])
#plt.hist(result)
print(collections.Counter(res_mode))
t2 = time.time()
print(t2-t1)