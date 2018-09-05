# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 09:41:49 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os

##　パスの設定
os.chdir(r"..\..\data")

##時間計測
t1 = time.time()

df_pt = pd.read_csv("PTdata.csv",encoding="SHIFT-JIS")

zone = np.unique(list(df_pt.Ozone) + list(df_pt.Dzone))

df_zone = pd.concat([df_pt.Ozone,df_pt.Dzone])

df_count = df_zone.value_counts()
df_count.sort_index(inplace=True)



##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")