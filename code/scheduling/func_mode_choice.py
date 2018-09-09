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

import numpy as np

##データの読み込み
from CSV_DATA import travel_time_dict, mode_para

##定数の読み込み
from CONSTANTS import MODE_LIST, MODE_INDEX


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
    result = np.random.choice(MODE_INDEX,n,p=mode_selection_probability(O,D))[0]
    ##パラメータ推定用の時間単位から換算する（* 1000）
    return MODE_LIST[result], travel_time_dict[(O,D)][result] * 1000


###検証用
#import time
#import collections
#import matplotlib.pyplot as plt
#t1 = time.time()
#O = 1
#D = 10
#res_mode, res_tt = zip(*[mode_choice(O,D) for x in range(1000)])
##plt.hist(result)
#print(collections.Counter(res_mode))
#t2 = time.time()
#print(t2-t1)