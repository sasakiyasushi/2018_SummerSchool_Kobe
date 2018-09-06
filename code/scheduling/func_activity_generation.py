# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:43:37 2018

@author: sasaki

活動作成の関数詰め合わせ

sample_home：自宅サンプリング関数
sample_frequency：活動回数のサンプリング
sample_start_time：活動開始時刻のサンプリング
sample_duration：活動継続時間のサンプリング

"""

import numpy as np

##データの読み込み
from CSV_DATA import home_sampling_list, frequency_dict, start_time_dict, duration_dict, frequency_arr

##定数の読み込み
from CONSTANTS import START_TIME_DELTA, START_TIME_LIST, DURATION_LIST

home_counter = 0

###自宅サンプリング関数
def sample_home():
    global home_counter
    home = home_sampling_list[home_counter]
    home_counter += 1
    return home


###活動回数のサンプリング
def sample_frequency(category, purpose):
    weight_list = frequency_dict[category][purpose]
    return np.random.choice(frequency_arr, 1, p=weight_list)[0]

###活動開始時刻のサンプリング
def sample_start_time(category, purpose, frequency):
    weight_list = start_time_dict[category][purpose][frequency]
    return np.random.choice(START_TIME_LIST, 1, p=weight_list)[0]
    
###活動継続時間のサンプリング
def sample_duration(category, purpose, start_time):
    weight_list =duration_dict[category][purpose][int(start_time/(START_TIME_DELTA*60))]
    return np.random.choice(DURATION_LIST, 1, p=weight_list)[0]


#####検証用
#import time
##時間計測
#t1 = time.time()
#import collections
##result = [sample_home() for i in range(10000000)]
##result = sample_home()
##print(collections.Counter(result))
#    
#category = "all_all"
#purpose = 1
#result = [sample_duration(category, purpose,sample_start_time(category,purpose,sample_frequency(category, purpose))) for i in range(1000)]
#
#print(collections.Counter(result))
###実行時間の出力
#t2 = time.time()
#elapsed_time = t2-t1
#print(f"実行時間：{elapsed_time}秒")