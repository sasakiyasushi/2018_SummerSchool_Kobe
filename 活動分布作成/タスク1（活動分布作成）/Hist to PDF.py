# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:59:33 2018

@author: nakano
"""

import os
import pandas as pd

os.chdir(r"E:/夏の学校2018/model2018/model2018/Japanese/配布データ/PTデータ/Result")

def JointPro(file_name):
    
    df = pd.read_csv(str(file_name),encoding="SHIFT-JIS",header=None)
    df = pd.concat([df,pd.DataFrame(df.sum(axis=0),columns=['Grand Total']).T])
    df = pd.concat([df,pd.DataFrame(df.sum(axis=1),columns=['Total'])],axis=1)

    summation = df.loc["Grand Total","Total"]
    
    df_pdf = pd.DataFrame(df/summation)
    
    df_pdf.to_csv(str("PDF_")+file_name,encoding="SHIFT-JIS",index= False)
    
    return df_pdf
    
JointPro("AF-ST_work_men.csv")