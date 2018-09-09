# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:28:45 2018

@author: sasaki

##グローバル変数の定義
"""


##再サンプリング上限回数
RESUMPLE_LIMIT = 10

##エピソードシフト上限時間(秒)
SHIFT_LIMIT = 2 * 60 * 60

##エピソード短縮　限界割合
SHORTENING_LIMIT = 0.5


##活動開始時間の時間の刻み(分)
START_TIME_DELTA = 30
##刻みインデックスに対する秒のリスト
START_TIME_LIST = list(range(0, 24*60*60, START_TIME_DELTA*60))
##刻みの数
START_TIME_NUM = len(START_TIME_LIST)

##活動継続時間の時間の刻み(分)
DURATION_DELTA = 15
##刻みインデックスに対する秒のリスト
##ただし，活動時間は似ないの平均をとるため，刻みの半分を足している
DURATION_LIST = list(range(0+int(DURATION_DELTA*60/2), 24*60*60+int(DURATION_DELTA*60/2), DURATION_DELTA*60))
##刻みの数
DURATION_NUM = len(DURATION_LIST)

##交通手段一覧
MODE_LIST = ["car","train","bus","cycle","walk"]

MODE_INDEX = list(range(len(MODE_LIST)))


##目的一覧
#PURPOSE_LIST = ["work", "school", "home", "shopping", "pastime", "others"]
PURPOSE_LIST = ["work", "school", "shopping", "pastime", "others"]

#PURPOSE_INDEX = list(range(1,len(PURPOSE_LIST)+1))
PURPOSE_INDEX = [1, 2, 4, 5, 6]

##目的のインデックスを文字列に変換する辞書
PURPOSE_DIC = dict(zip(PURPOSE_INDEX, PURPOSE_LIST))


##個人属性分類一覧
AGE_LIST = ["all", "under20", "over70", "20to69"]
SEX_LIST = ["all", "men", "women"]

CATEGORY_LIST = [f"{age}_{sex}" for age in AGE_LIST for sex in SEX_LIST]

"""
CATEGORY_LIST
['all_all', 'all_men', 'all_women', 'under20_all', 'under20_men', 'under20_women',
 'over70_all', 'over70_men', 'over70_women', '20to69_all', '20to69_men', '20to69_women']
"""


##結果用のカラム名

RES_COL = ["personalID", "activityID", "O", "trip_start", "travel_time",\
           "mode", "D", "purpose", "activity_start", "activity_end"]