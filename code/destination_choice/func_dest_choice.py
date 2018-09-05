# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 08:49:06 2018

@author: sasaki

目的地選択関数
dest_choice

引数
purpose : ["work","school","shopping","pastime","others"]
O : 起点ID
n : 目的地選択個数（デフォルトで1）

"""

import pandas as pd
import numpy as np
import os

##　パスの設定
os.chdir(r"..\..\data\choice")

##データの読み込み
df_dis = pd.read_csv("distance.csv", encoding="SHIFT-JIS")
df_zone = pd.read_csv("zone.csv", encoding="SHIFT-JIS",index_col=[0])
df_dest_para = pd.read_csv("para_dest.csv", encoding="SHIFT-JIS",index_col=[0])

##zoneの地理的特徴を辞書に格納(速度向上のため)
zone_dict = df_zone.to_dict(orient="dict")

##目的別のパラメータを辞書に格納(速度向上のため)
dest_para = df_dest_para.to_dict(orient="dict")


##効用関数(実際の推定結果に合わせて変更予定)
def dest_utility_function(purpose, D, distance):
    return dest_para[purpose]["B_dist"] * distance + dest_para[purpose][f"C_{D:03d}"] + dest_para[purpose]["B_v"] * zone_dict[f"v_{purpose}"][D]


##選択確率の計算
def dest_selection_probability(purpose,O,D,dist):
    ##効用配列
    V = np.vectorize(dest_utility_function)(purpose, D, dist)
    return np.exp(V) / np.exp(V).sum(axis=0)


##目的地選択関数(目的地選択個数をnで指定)
def dest_choice(purpose,O,n=1):
    ##インプット用配列作成
    D, dist = df_dis[df_dis.O == O][["D","dist"]].values.T
    ##重み付き復元抽出
    return np.random.choice(D,n,p=dest_selection_probability(purpose,O,D,dist))


###検証用
#import time
#import collections
#import matplotlib.pyplot as plt
#t1 = time.time()
#O = 1
#purpose = "work"
#n = 1
#result = [dest_choice(purpose,O,n)[0] for x in range(1000)]
#plt.hist(result)
#print(collections.Counter(result))
#t2 = time.time()
#print(t2-t1)