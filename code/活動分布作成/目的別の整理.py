
#目的番号を振り直し
"""
元の対応
1:勤務先へ
2:通学先へ
3:自宅へ
4:買い物へ
5:食事・社交・娯楽へ
6:観光・行楽・レジャーへ
7:通院
8:その他の私用へ
9:送迎
10:販売・配達・仕入・購入先へ
11:打合せ・会議・集会・往診へ
12:作業・修理へ
13:農林漁業作業へ
14:その他の業務へ
99:不明
"""

# 目的別の整理
# １．通勤
# ２．通学
# ３．帰宅（自宅）
# ４．買い物
# ５．娯楽
# ６．その他

import os
import pandas as pd
os.chdir(r"..\data")

df = pd.read_csv("PTdata.csv",encoding="SHIFT-JIS")


##目的をまとめる
others_list = [7,8,9,10,11,12,13,14,99]

df["Purpose"] = df["Purpose"].replace(6,5)

for i in others_list:
    df["Purpose"] = df["Purpose"].replace(i,6)

##ファイルの書き出し
df.to_csv("PTdata2.csv",encoding="SHIFT-JIS",index= False)
