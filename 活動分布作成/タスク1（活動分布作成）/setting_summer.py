# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 15:07:04 2018

@author: nakano
"""

import pandas as pd

"""
data = df1,df2
purpose = "work","school" 等
category = "women","under20" 等
"""

def Dataframe(data,purpose,category):
    
    #目的別
    df_work = pd.DataFrame(data[data["Purpose"].isin(["1"])])
    df_school = pd.DataFrame(data[data["Purpose"].isin(["2"])])
    df_home = pd.DataFrame(data[data["Purpose"].isin(["3"])])
    df_shopping = pd.DataFrame(data[data["Purpose"].isin(["4"])])
    df_pastime = pd.DataFrame(data[data["Purpose"].isin(["5"])])
    df_others = pd.DataFrame(data[data["Purpose"].isin(["6"])])
    
    df_purpose = locals()["df_"+ str(purpose)]
    
    ##個人別
    #性別データ
    df_men = pd.DataFrame(df_purpose[df_purpose["Sex"].isin(["1"])])
    df_women = pd.DataFrame(df_purpose[df_purpose["Sex"].isin(["2"])])
    
    #年齢データ
    df_under20 = pd.DataFrame(df_purpose[df_purpose["Age"].isin(["1","2","3"])])
    df_over70 = pd.DataFrame(df_purpose[df_purpose["Age"].isin(["14","15","16","17"])])
    df_20to69 = pd.DataFrame(df_purpose[df_purpose["Age"].isin(["4","5","6","7","8","9","10","11","12","13"])])
    
    #性別複合
    df_over70_men = pd.DataFrame(df_over70[df_over70["Sex"].isin(["1"])])
    df_over70_women = pd.DataFrame(df_over70[df_over70["Sex"].isin(["2"])])
    df_20to69_men = pd.DataFrame(df_20to69[df_20to69["Sex"].isin(["1"])])
    df_20to69_women = pd.DataFrame(df_20to69[df_20to69["Sex"].isin(["2"])])
    df_under20_men = pd.DataFrame(df_men[df_men["Age"].isin(["1","2","3"])])
    df_under20_women = pd.DataFrame(df_women[df_women["Age"].isin(["1","2","3"])])
    
    df = locals()["df_" + str(category)]
    
    return df