# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 13:45:36 2018

@author: sasaki
"""


import pandas as pd
import numpy as np
import time
import os

##時間計測
t1 = time.time()

##　パスの設定
os.chdir(r"..\..\data\input_data")

personal_id = list(range(100000))
sex = ["all"] * len(personal_id)
age = ["all"] * len(personal_id)

df = pd.DataFrame(list(zip(personal_id,sex,age)),columns=["id","sex","age"])

df.to_csv("personal_data.csv", index=False)

##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")