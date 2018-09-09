# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 10:36:20 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os

##時間計測
t1 = time.time()


##　パスの設定
os.chdir(r".\choice")

##ゾーン数の設定
zone_num = 100

###ゾーンの地理的特徴一覧
#df_zone = pd.DataFrame(list(range(zone_num)), columns=["zoneID"])
#df_zone["population"] = [100] * zone_num
#df_zone[["v_work","v_school","v_shopping","v_pastime","v_others"]] = pd.DataFrame([(1,1,1,1,1)] * zone_num)
#
#df_zone.to_csv("zone.csv", index=False)
#
###ゾーン間距離
#od_pair = [(x,y) for y in range(zone_num) for x in range(zone_num)]
#df_dist = pd.DataFrame(od_pair, columns=["O","D"])
#df_dist["dist"] = [5] * len(od_pair)
#
#df_dist.to_csv("distance.csv", index=False)
#
#
##ゾーン間旅行時間（交通手段別）
#df_time = pd.DataFrame(od_pair, columns=["O","D"])
#df_time[["car","train","bus","cycle","walk"]] = pd.DataFrame([(1,2,3,4,5)] * len(od_pair))
#
#df_time.to_csv("travel_time.csv", index=False)
#
###パラメータ推定結果作成
##目的地選択
#dest_para = {"B_dist":(1,1,1,1,1),"B_v":(2,2,2,2,2)}
#for i in range(zone_num-1):
#    dest_para[f"C_{i:03d}"] = (1,1,1,1,1)
###一つだけ定数項パラメータがない目的地がある
#dest_para[f"C_{zone_num-1:03d}"] = (0,0,0,0,0)
#df_dest_para = pd.DataFrame.from_dict(dest_para, orient='index')
#df_dest_para.columns = ["work","school","shopping","pastime","others"]
#df_dest_para.to_csv("para_dest.csv")
#
##交通手段選択
#mode_para = {"B_time":1,"C_car":1,"C_train":1,"C_bus":1,"C_cycle":1}
#df_mode_para = pd.DataFrame.from_dict(mode_para, orient='index')
#df_mode_para.to_csv("para_mode.csv")


##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")