# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:48:21 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os

##　パスの設定
os.chdir(r"..\data")

##時間計測
t1 = time.time()



##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")