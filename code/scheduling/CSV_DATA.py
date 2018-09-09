# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:57:12 2018

@author: sasaki

ファイルの読み込みを一括で管理
"""

import pandas as pd
import numpy as np
import os

##定数の読み込み
from CONSTANTS import CATEGORY_LIST, PURPOSE_INDEX, START_TIME_NUM, DURATION_NUM

##後で戻すため，現在のディレクトリを保存
cd = os.getcwd()

##　パスの設定
os.chdir(r"..\..\data\input_data")

df_personal = pd.read_csv("personal_data.csv", encoding="SHIFT-JIS")

PEOPLE_NUM = len(df_personal)

id_arr = df_personal.id.values
sex_arr = df_personal.sex.values
age_arr = df_personal.age.values
category_arr = np.vectorize(lambda x, y: f"{x}_{y}")(age_arr, sex_arr)


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

##確率分布を辞書に格納
frequency_dict = {}
start_time_dict = {}
duration_dict = {}

for category in CATEGORY_LIST:
    frequency_dict[category] = {}
    start_time_dict[category] = {}
    duration_dict[category] = {}
    for purpose in PURPOSE_INDEX:
        cp = f"{category}_{purpose}"
        
        df_fre = pd.read_csv(f"frequency_{cp}.csv",index_col=["frequency"])
        tmp_fre = df_fre.values.flatten()
        frequency_dict[category][purpose] = tmp_fre
        
        df_sta = pd.read_csv(f"start_time_{cp}.csv",index_col=["frequency"])
        tmp_sta = df_sta.values
        start_time_dict[category][purpose] = tmp_sta[:,:START_TIME_NUM]
        
        df_dur = pd.read_csv(f"duration_{cp}.csv",index_col=["start_time"])
        tmp_dur = df_dur.values
        duration_dict[category][purpose] = tmp_dur[:,:DURATION_NUM]
else:
    frequency_arr = df_fre.index.values
    start_time_arr = np.vectorize(np.int64)(df_sta.columns.values)
    duration_arr = np.vectorize(np.int64)(df_dur.columns.values)

##ディレクトリを元に戻す
os.chdir(cd)