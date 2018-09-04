# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:11:17 2018

@author: nakano
"""

import os
import pandas as pd
import datetime

t=datetime.time(2,30)
os.chdir(r"C:/Users/nakano/Desktop/夏の学校")

#列
#df1 = pd.read_csv("PTdata1.csv",encoding="SHIFT-JIS")
df2 = pd.read_csv("PTdata2.csv",encoding="SHIFT-JIS")

#活動数分布
name = "2"
#name = "_over70_men"

df2_named =  locals()["df"+name]
df2_person = df2_named.drop_duplicates(['TripChainID'])

df2_named['Total Stay Time']=0

for i in range(len(df2_named)):
    print(i)
    TCID = df2_named['TripChainID'][i]
    df2_named['Total Stay Time'][i] = df2_named[df2_named['TripChainID'] ==TCID]["StayTime"].sum()

df2_named.to_csv("PTdata3.csv",encoding="SHIFT-JIS",index= False)
    