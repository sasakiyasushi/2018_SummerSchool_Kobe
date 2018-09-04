# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:59:33 2018

@author: nakano
"""

import os
import pandas as pd
import time

##時間計測
t1 = time.time()

##ディレクトリの設定
os.chdir(r"..\..\..\data\Hist")
##Histフォルダにあるファイルをすべて取得
file_list = os.listdir()

##出力先ディレクトリの作成
parent_file_list = os.listdir(r"..")
if "PDF" not in parent_file_list:
    os.mkdir(r"..\PDF")
    
    
def JointPro(file_name):
    
    df = pd.read_csv(str(file_name),encoding="SHIFT-JIS",header=None)
    df = pd.concat([df,pd.DataFrame(df.sum(axis=0),columns=['Grand Total']).T])
    df = pd.concat([df,pd.DataFrame(df.sum(axis=1),columns=['Total'])],axis=1)

    summation = df.loc["Grand Total","Total"]
    
    df_pdf = pd.DataFrame(df/summation)
    
    df_pdf.to_csv(r"..\PDF\PDF_"+file_name,encoding="SHIFT-JIS",index= False)
    
    return df_pdf


for file_name in file_list:
    JointPro(file_name)


##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")