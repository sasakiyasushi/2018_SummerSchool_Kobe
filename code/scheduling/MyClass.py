# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:51:37 2018

@author: sasaki

クラスの定義
"""

import numpy as np

##定数の読み込み
from CONSTANTS import SHIFT_LIMIT, SHORTENING_LIMIT, PURPOSE_INDEX, PURPOSE_DIC

##外部の関数読み込み
from func_activity_generation import sample_home, initial_sampling
from func_mode_choice import mode_choice
from func_dest_choice import dest_choice



class Episode:
    def __init__(self, start_time, duration, purpose):
        self.__INITIAL_START_TIME = start_time
        self.__INITIAL_DURATION = duration
        self.__START_TIME_MIN = start_time - SHIFT_LIMIT
        self.__START_TIME_MAX = start_time + SHIFT_LIMIT
        self.__DURATION_MIN = duration * SHORTENING_LIMIT
        
        self.__PURPOSE = purpose
        
        self.__start_time = start_time
        self.__duration = duration
        
        self.__pre_start_time = start_time
        self.__pre_duration = duration
        
        ##活動前トリップに関する変数
        self.__place = -1
        self.__mode = "none"
        self.__travel_time = -1
        
    def get_MAX(self):
        return self.__START_TIME_MAX
    def get_MIN(self):
        return self.__START_TIME_MIN
        
    def get_purpose(self):
        return self.__PURPOSE
    def get_start_time(self):
        return self.__start_time
    def get_duration(self):
        return self.__duration
    def get_end_time(self):
        return self.__start_time + self.__duration
    def get_pre_start_time(self):
        return self.__pre_start_time
    def get_pre_duration(self):
        return self.__pre_duration
    def get_pre_end_time(self):
        return self.__pre_start_time + self.__pre_duration
    def get_gap(self, ep): ##重なっている場合は負，離れている場合は正
        min_t = min(self.__pre_start_time, ep.get_pre_start_time())
        max_t = max(self.get_pre_end_time(), ep.get_pre_end_time())
        return (max_t - min_t) - (self.__pre_duration + ep.get_pre_duration())
            
    def update(self):
        self.__start_time = self.__pre_start_time
        self.__duration = self.__pre_duration
    def downdate(self):
        self.__pre_start_time = self.__start_time
        self.__pre_duration = self.__duration
        
    def shift(self, s):
        if self.__START_TIME_MIN > self.__pre_start_time + s:
            self.__pre_start_time = self.__START_TIME_MIN
        elif self.__START_TIME_MAX < self.__pre_start_time + s:
            self.__pre_start_time = self.__START_TIME_MAX
        else:
            self.__pre_start_time += s
    def shortening(self, d):
        if self.__DURATION_MIN < self.__pre_duration + d:
            self.__pre_duration += d
        else:
            self.__pre_duration = self.__DURATION_MIN
    
    ##活動前トリップに関するメソッド
    def get_place(self):
        return self.__place
    def get_mode(self):
        return self.__mode
    def get_travel_time(self):
        return self.__travel_time
    def get_t_start_time(self):
        return self.__start_time - self.__travel_time
    def get_t_pre_start_time(self):
        return self.__pre_start_time - self.__travel_time
    def get_t_gap(self, ep):
        min_t = min(self.get_t_pre_start_time(), ep.get_t_pre_start_time())
        max_t = max(self.get_pre_end_time(), ep.get_pre_end_time())
        return (max_t - min_t) - (self.__pre_duration + ep.get_pre_duration() + self.__travel_time + ep.get_travel_time())
    
    def set_place(self, O):
        self.__place = dest_choice(self.__PURPOSE, O)
        self.__mode, self.__travel_time = mode_choice(O, self.__place)
    def forced_shift(self, s): ##強制シフト
        self.__pre_start_time += s
    
    ##確認用
    def output(self):
        return self.__start_time, self.get_end_time()



class Project:
    def __init__(self, category, purpose):
        self.__frequency, start_time_list, duration_list = initial_sampling(category, purpose)
        self.pre_schedule = [Episode(st,du,purpose) for st, du in zip(start_time_list, duration_list)]
        self.schedule = []
        
    def get_frequency(self):
        return self.__frequency

    def schedule_episode(self, new_episode):
#        print("挿入するエピソード", new_episode.output())
#        print("挿入される前のスケジュール", [x.output() for x in self.schedule])
        overlap_list = [] ## 新しく挿入するエピソードと時間の被りがあるエピソード
        prior_ind = -1 ## 新しく挿入するエピソードの前のエピソード
        for i, epi in enumerate(self.schedule):
            if epi.get_start_time() <= new_episode.get_start_time():
                prior_ind = i ##開始時間が新しく挿入するエピソードより前の場合，indexを更新
            if not(new_episode.get_end_time() <= epi.get_start_time() or epi.get_end_time() <= new_episode.get_start_time()):
                overlap_list.append(i)
        overlap_num = len(overlap_list)
        if overlap_num == 0: ##時間的に被りがない場合，新しいエピソードを挿入
            self.schedule.insert(prior_ind+1, new_episode)
        elif overlap_num == 1: ##一つのエピソードのみが重なっているとき
            overlap_ind = overlap_list[0]
            if self.schedule[overlap_ind].get_start_time() <= new_episode.get_start_time() and new_episode.get_end_time() <= self.schedule[overlap_ind].get_end_time():
                ## 挿入するエピソードが，既存のエピソードに内包されている場合は排除
                pass
            else:
                if overlap_ind == prior_ind: ##重なっているのが前のエピソード
                    gap = new_episode.get_gap(self.schedule[overlap_ind])
                    ###### 挿入するエピソードのシフト
                    if overlap_ind == len(self.schedule) - 1: ##重なっているエピソードが末尾
#                        print("a")
                        new_episode.shift(-1 * gap)
                    else:
#                        print("b")
                        new_episode.shift(min(abs(gap),new_episode.get_gap(self.schedule[overlap_ind+1])))
                    gap = new_episode.get_gap(self.schedule[overlap_ind])
                    if gap <  0:
                        ###### 前のエピソードをシフト
                        if overlap_ind == 0: ## 重ねってるエピソードが先頭
                            self.schedule[overlap_ind].shift(gap)
                        else:
                            self.schedule[overlap_ind].shift(max(gap, -1 * self.schedule[overlap_ind].get_gap(self.schedule[overlap_ind-1])))
                        gap = new_episode.get_gap(self.schedule[overlap_ind])
                        if gap <  0:
                            ###### 挿入するエピソードを削減
                            new_episode.shortening(gap)
                            if overlap_ind == len(self.schedule) - 1: ##重なっているエピソードが末尾
#                                print("c")
                                new_episode.shift(abs(new_episode.get_gap(self.schedule[overlap_ind])))
                            else:
#                                print("d")
                                new_episode.shift(min(abs(new_episode.get_gap(self.schedule[overlap_ind])),new_episode.get_gap(self.schedule[overlap_ind+1])))
                            gap = new_episode.get_gap(self.schedule[overlap_ind])
                            if gap <  0:
                                ###### 前のエピソードを削減
                                self.schedule[overlap_ind].shortening(gap)
                                gap = new_episode.get_gap(self.schedule[overlap_ind])
                                if gap <  0:
                                    ##重なりが解消できなかった時
                                    new_episode.downdate()
                                    self.schedule[overlap_ind].downdate()
                                    return
                    ##重なりが解消できたとき(念のための確認をするコードを入れてもよいが速度が心配)
                    new_episode.update()
                    self.schedule[overlap_ind].update()
                    self.schedule.insert(prior_ind+1, new_episode)
                else: ##重なっているのが後ろのエピソード
                    gap = new_episode.get_gap(self.schedule[overlap_ind])
                    ###### 挿入するエピソードのシフト
                    if overlap_ind == 0: ##重なっているエピソードが先頭
#                        print("e")
                        new_episode.shift(gap)
                    else:
#                        print("f")
                        new_episode.shift(max(gap, -1 * new_episode.get_gap(self.schedule[overlap_ind-1])))
                    gap = new_episode.get_gap(self.schedule[overlap_ind])
                    if gap <  0:
                        ###### 後ろのエピソードをシフト
                        if overlap_ind == len(self.schedule) - 1: ## 重ねってるエピソードが末尾
                            self.schedule[overlap_ind].shift(-1 * gap)
                        else:
                            self.schedule[overlap_ind].shift(min(abs(gap), self.schedule[overlap_ind].get_gap(self.schedule[overlap_ind+1])))
                        gap = new_episode.get_gap(self.schedule[overlap_ind])
                        if gap <  0:
                            ###### 挿入するエピソードを削減
                            new_episode.shortening(gap)
                            gap = new_episode.get_gap(self.schedule[overlap_ind])
                            if gap <  0:
                                ###### 後ろのエピソードを削減
                                self.schedule[overlap_ind].shortening(gap)
                                if overlap_ind == len(self.schedule) - 1: ##重なっているエピソードが末尾
                                    self.schedule[overlap_ind].shift(gap)
                                else:
                                    self.schedule[overlap_ind].shift(min(abs(gap), self.schedule[overlap_ind].get_gap(self.schedule[overlap_ind+1])))
                                gap = new_episode.get_gap(self.schedule[overlap_ind])
                                if gap <  0:
                                    ##重なりが解消できなかった時
                                    new_episode.downdate()
                                    self.schedule[overlap_ind].downdate()
                                    return
                    ##重なりが解消できたとき
                    new_episode.update()
                    self.schedule[overlap_ind].update()
                    self.schedule.insert(prior_ind+1, new_episode)
                    
            
        elif overlap_num == 2: ##被りが二つ以上
#            print("2")
            overlap_pri = overlap_list[0] ##一つ目のインデックス
            overlap_pos = overlap_list[1] ##二つ目のインデックス
            if new_episode.get_start_time() <= self.schedule[overlap_pri].get_start_time() or self.schedule[overlap_pos].get_end_time() <= new_episode.get_end_time():
                ##挿入するエピソードが一つでも既存のエピソードを内包する場合は排除
                return
            else:
                gap = new_episode.get_gap(self.schedule[overlap_pri]) + new_episode.get_gap(self.schedule[overlap_pos])
                ###### 前のエピソードをシフト
                if overlap_pri == 0: ## 重なってるエピソードが先頭
                    self.schedule[overlap_pri].shift(gap)
                else:
                    self.schedule[overlap_pri].shift(max(gap, -1 * self.schedule[overlap_pri].get_gap(self.schedule[overlap_pri-1])))
                ##前のエピソードがずれてできた隙間の分だけ挿入するエピソードもシフト
#                print("g")
                if new_episode.get_gap(self.schedule[overlap_pri]) > 0:
                    new_episode.shift(-1 * new_episode.get_gap(self.schedule[overlap_pri]))
                gap_pri = new_episode.get_gap(self.schedule[overlap_pri])
                gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                gap = (gap_pri < 0) * gap_pri + (gap_pos < 0) * gap_pos
                if gap <  0:
                    ###### 後ろのエピソードをシフト
                    if overlap_pos == len(self.schedule) - 1: ## 重ねってるエピソードが末尾
                        self.schedule[overlap_pos].shift(-1 * gap)
                    else:
                        self.schedule[overlap_pos].shift(min(abs(gap), self.schedule[overlap_pos].get_gap(self.schedule[overlap_pos+1])))
                    ##後ろのエピソードがずれてできた隙間の分だけ挿入するエピソードもシフト
#                    print("h")
                    if new_episode.get_gap(self.schedule[overlap_pos]) > 0:
                        new_episode.shift(new_episode.get_gap(self.schedule[overlap_pos]))
                    gap_pri = new_episode.get_gap(self.schedule[overlap_pri])
                    gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                    gap = (gap_pri < 0) * gap_pri + (gap_pos < 0) * gap_pos
                    if gap < 0:
                        ###### 挿入するエピソードを削減
                        new_episode.shortening(gap)
                        gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                        if gap_pos >= 0:
#                            print("i")
                            new_episode.shift(min(abs(new_episode.get_gap(self.schedule[overlap_pri])),new_episode.get_gap(self.schedule[overlap_pos])))
                        gap_pri = new_episode.get_gap(self.schedule[overlap_pri])
                        gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                        gap = (gap_pri < 0) * gap_pri + (gap_pos < 0) * gap_pos
                        if gap < 0:
                            ###### 前のエピソードを削減
                            self.schedule[overlap_pri].shortening(gap)
                            ##前のエピソードがずれてできた隙間の分だけ挿入するエピソードもシフト
#                            print("j")
                            if new_episode.get_gap(self.schedule[overlap_pri]) > 0:
                                new_episode.shift(-1 * new_episode.get_gap(self.schedule[overlap_pri]))
                            gap_pri = new_episode.get_gap(self.schedule[overlap_pri])
                            gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                            gap = (gap_pri < 0) * gap_pri + (gap_pos < 0) * gap_pos
                            if gap < 0:
                                ###### 後ろのエピソードを削減
                                self.schedule[overlap_pos].shortening(gap)
                                if overlap_pos == len(self.schedule) - 1: ##重なっているエピソードが末尾
                                    self.schedule[overlap_pos].shift(-1 * gap)
                                else:
                                    self.schedule[overlap_pos].shift(min(abs(gap), self.schedule[overlap_pos].get_gap(self.schedule[overlap_pos+1])))
                                ##後ろのエピソードがずれてできた隙間の分だけ挿入するエピソードもシフト
                                if new_episode.get_gap(self.schedule[overlap_pos]) > 0:
                                    new_episode.shift(new_episode.get_gap(self.schedule[overlap_pos]))
                                gap_pri = new_episode.get_gap(self.schedule[overlap_pri])
                                gap_pos = new_episode.get_gap(self.schedule[overlap_pos])
                                gap = (gap_pri < 0) * gap_pri + (gap_pos < 0) * gap_pos
                                if gap <  0:
                                    ##重なりが解消できなかった時
                                    new_episode.downdate()
                                    self.schedule[overlap_pri].downdate()
                                    self.schedule[overlap_pos].downdate()
                                    return
                ##重なりが解消できたとき
                new_episode.update()
                self.schedule[overlap_pri].update()
                self.schedule[overlap_pos].update()
                self.schedule.insert(overlap_pos, new_episode)
                            
        else: ## 被りが三つ以上ある場合は，新しいエピソードが既存のエピソードを内包しているということなので排除
            pass
#        print("挿入された後のスケジュール", [x.output() for x in self.schedule])
    
    def make_schedule(self):
        for episode in self.pre_schedule:
            self.schedule_episode(episode)
            ##プロジェクト内のエピソードが活動数に達したら終了
            if len(self.schedule) == self.__frequency:
                break
    


class Schedule(Project):
    ###Projectクラスを継承
    def __init__(self, ID, category):
        self.__personal_id = ID
        self.__home = sample_home()
        self.projects = [Project(category, purpose) for purpose in PURPOSE_INDEX]
        self.pre_schedule = []
        ex = self.pre_schedule.extend ##メソッドをキャッシュ
        for pro in self.projects:
            pro.make_schedule()
            ex(pro.schedule)
        self.schedule = []
        self.__go_home_trip = {}
        
    def get_home(self):
        return self.__home
    
    ##出力用
    def to_list(self):
        ##結果をリストにまとめて表示
        result = []
        O = self.__home
        ap = result.append ##メソッドをキャッシュ
        for i, e in enumerate(self.schedule):
            ##個人ＩＤ，アクティビティID，出発地，トリップ開始時刻，旅行時間，交通手段，
            ##到着地（活動場所），目的，活動開始時間，活動終了時間
            res = (self.__personal_id, i, O, e.get_t_start_time(), e.get_travel_time(), e.get_mode(),\
                   e.get_place(), PURPOSE_DIC[e.get_purpose()], e.get_start_time(), e.get_end_time())
            O = e.get_place()
            ap(res)
        ##　帰宅トリップの記述
        res = (self.__personal_id, i+1, O, e.get_end_time(), self.__go_home_trip["travel_time"],\
               self.__go_home_trip["mode"], self.__home, np.nan, np.nan, np.nan)
        ap(res)
        return result
    
#    ##確認用
#    def out_put(self):
#        for e in self.schedule:
#            print(e.get_purpose(), e.get_start_time(), e.get_duration(), e.get_end_time())     
#    def out_put2(self):
#        for e in self.schedule:
#            print(e.get_purpose(), e.get_t_start_time(), e.get_duration(), e.get_end_time(), e.get_travel_time())
            
    def make_schedule(self):
        sc = self.schedule_episode ##メソッドをキャッシュ
        for episode in self.pre_schedule:
            sc(episode)
            
    def front_shift(self, overlap): ##スケジュールを前方にずらす
        for i, eps in enumerate(self.schedule):
            if i == 0: ##先頭スケジュール
                eps.shift(overlap)
            else:
                ##前方エピソードとのギャップがある場合，シフト
                gap = eps.get_t_gap(self.schedule[i-1])
                if gap > 0:
                    eps.shift(max(overlap, -1 * gap))
    def rear_shift(self, overlap): ##スケジュールを後方にずらす
        for i, eps in enumerate(self.schedule[::-1]):
            ##スケジュールを逆順にループ
            if i == 0: ##末尾スケジュール
                eps.shift(-1 * overlap)
            else:
                ##後方エピソードとのギャップがある場合，シフト
                gap = eps.get_t_gap(self.schedule[len(self.schedule) - i])
                if gap > 0:
                    eps.shift(min(-1 * overlap, gap))
                    
    def insert_trip(self):
        ##活動場所，旅行時間，交通手段の設定
        place_list = [sample_home()]
        ap = place_list.append ##メソッドをキャッシュ
        for e in self.schedule:
            e.set_place(place_list[-1])
            ap(e.get_place())
        ##帰宅トリップの設定
        self.__go_home_trip["mode"] , self.__go_home_trip["travel_time"] = mode_choice(place_list[-1], self.__home)
        ##スケジュール調整
        gap_list = [self.schedule[i].get_t_gap(self.schedule[i+1]) for i in range(len(self.schedule)-1)]
#        print(gap_list)
        gap_flag = [g >= 0 for g in gap_list]
        if sum(gap_flag) == len(gap_flag):
            for e in self.schedule:
                e.update()
            return ##ギャップが全て正なら終了
        ######## ずらすことによる調整
        overlap = sum([x for x in gap_list if x < 0])
        self.front_shift(overlap)
        self.rear_shift(overlap)
        gap_list = [self.schedule[i].get_t_gap(self.schedule[i+1]) for i in range(len(self.schedule)-1)]
        gap_flag = [g >= 0 for g in gap_list]
        if sum(gap_flag) == len(gap_flag):
            for e in self.schedule:
                e.update()
            return ##ギャップが全て正なら終了
        ######## 活動時間を削減することによる調整
        overlap = sum([x for x in gap_list if x < 0])
        ##活動時間が長いものから削減
        duration_sorted_index = list(np.argsort([e.get_pre_duration() for e in self.schedule]))
        for i in duration_sorted_index:
            self.schedule[i].shortening(overlap)
            self.front_shift(overlap)
            self.rear_shift(overlap)
            gap_list = [self.schedule[i].get_t_gap(self.schedule[i+1]) for i in range(len(self.schedule)-1)]
            gap_flag = [g >= 0 for g in gap_list]
            if sum(gap_flag) == len(gap_flag):
                for e in self.schedule:
                    e.update()
                return ##ギャップが全て正なら終了
            overlap = sum([x for x in gap_list if x < 0])
        ####### 制限を超えてずらす（最終調整）
        for i, eps in enumerate(self.schedule):
            if i == 0: ##先頭スケジュール
                eps.forced_shift(overlap)
            else:
                ##前方エピソードとのギャップがある場合，シフト
                gap = eps.get_t_gap(self.schedule[i-1])
                if gap > 0:
                    eps.forced_shift(max(overlap, -1 * gap))
        for i, eps in enumerate(self.schedule[::-1]):
            ##スケジュールを逆順にループ
            if i == 0: ##末尾スケジュール
                eps.forced_shift(-1 * overlap)
            else:
                ##後方エピソードとのギャップがある場合，シフト
                gap = eps.get_t_gap(self.schedule[len(self.schedule) - i])
                if gap > 0:
                    eps.forced_shift(min(-1 * overlap, gap))
        ##最終チェック
        gap_list = [self.schedule[i].get_t_gap(self.schedule[i+1]) for i in range(len(self.schedule)-1)]
#        print(gap_list)
        gap_flag = [g >= 0 for g in gap_list]
        for e in self.schedule:
            e.update()
        if sum(gap_flag) == len(gap_flag):
            return
        else:
            ##ギャップが解消されない場合，エラー表示
            print("OVERLAP_ERROR", self.__perspnal_id)
        


###検証用
#import time
#t1 = time.time()
#
#schedule_list = []
#        
#for i in range(100):
#    s = Schedule(i, "all_all")
#    s.make_schedule()
##    print(len(s.pre_schedule), len(s.schedule))
##    s.out_put()
##    print()
#    s.insert_trip()
##    s.out_put()
##    print()
##    s.out_put2()
#    schedule_list.append(s)
##    print()
#
###実行時間の出力
#t2 = time.time()
#elapsed_time = t2-t1
#print(f"実行時間：{elapsed_time}秒")
