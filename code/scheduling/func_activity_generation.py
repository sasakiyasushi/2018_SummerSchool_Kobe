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

import pandas as pd
import numpy as np
import os

##データの読み込み
from CSV_DATA import home_sampling_list

home_counter = 0

###自宅サンプリング関数
def sample_home():
    global home_counter
    home = home_sampling_list[home_counter]
    home_counter += 1
    return home


    
#def sample_frequency():
#    
#    
#def sample_start_time():
#    
#    
#def sample_duration():
    


#####検証用
#import time
##時間計測
#t1 = time.time()
#import collections
##result = [sample_home() for i in range(10000000)]
#result = sample_home()
#print(collections.Counter(result))
#
#
###実行時間の出力
#t2 = time.time()
#elapsed_time = t2-t1
#print(f"実行時間：{elapsed_time}秒")