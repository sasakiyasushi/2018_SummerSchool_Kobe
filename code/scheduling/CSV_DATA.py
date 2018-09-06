# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:57:12 2018

@author: sasaki

ファイルの読み込みを一括で管理
"""

import pandas as pd
import numpy as np
import os


##　パスの設定
os.chdir(r"..\..\data\input_data")

df_personal = pd.read_csv("personal_data.csv", encoding="SHIFT-JIS", index_col=[0])

PEOPLE_NUM = len(df_personal)


##　パスの設定
os.chdir(r"..\choice")

##### mode_choice

##旅行時間
df_travel_time = pd.read_csv("travel_time.csv", encoding="SHIFT-JIS",index_col=[0,1])
##旅行時間を辞書に格納(速度向上のため)
travel_time_dict = df_travel_time.T.to_dict(orient="list")

##mode_choiceのパラメータ
df_mode_para = pd.read_csv("para_mode.csv", encoding="SHIFT-JIS",index_col=[0])
##目的別のパラメータを辞書に格納(速度向上のため)
mode_para = df_mode_para.iloc[:,0].to_dict()



##### dest_choice

##OD間の距離
df_distance = pd.read_csv("distance.csv", encoding="SHIFT-JIS")

##zoneの地理的特徴
df_zone = pd.read_csv("zone.csv", encoding="SHIFT-JIS",index_col=["zoneID"])
##zoneの地理的特徴を辞書に格納(速度向上のため)
zone_dict = df_zone.to_dict(orient="dict")

##destination_choiceのパラメータ
df_dest_para = pd.read_csv("para_dest.csv", encoding="SHIFT-JIS",index_col=[0])
##目的別のパラメータを辞書に格納(速度向上のため)
dest_para = df_dest_para.to_dict(orient="dict")



##### activity_genaration
#人口データ
df_population = df_zone["population"]
##ゾーンＩＤ一覧
zone_arr = np.array(df_population.index)
pop_arr = np.array(df_population)
##重み一覧
pop_w = pop_arr / pop_arr.sum()

##事前に家のリストを作成(PEOPLE_NUMに余裕をもって100足しとく)
home_sampling_list = np.random.choice(zone_arr, PEOPLE_NUM+100, p=pop_w)

##　パスの設定
os.chdir(r"..\activity_generation")

