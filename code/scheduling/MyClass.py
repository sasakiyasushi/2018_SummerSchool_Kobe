# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:51:37 2018

@author: sasaki

クラスの定義
"""

##定数の読み込み
from CONSTANTS import SHIFT_LIMIT, SHORTENING_LIMIT

##外部の関数読み込み
from func_activity_generation import sample_home, initial_sampling
#from func_mode_choice import mode_choice
#from func_dest_choice import dest_choice



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
        self.__place = -1
        
        self.__pre_start_time = start_time
        self.__pre_duration = duration
        
    def get_start_time(self):
        return self.__start_time
    def get_duration(self):
        return self.__duration
    def get_end_time(self):
        return self.__start_time + self.__duration
    def get_place(self):
        return self.__place
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
    
    def set_place(self, p):
        self.__place = p
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
        
    def output(self):
        return self.__start_time, self.get_end_time()



class Project:
    def __init__(self, category, purpose):
        self.__frequency, start_time_list, duration_list = initial_sampling(category, purpose)
        self.__frequency = 4
        self.pre_schedule = [Episode(st,du,purpose) for st, du in zip(start_time_list, duration_list)]
        self.schedule = []
        
    def get_frequency(self):
        return self.__frequency
    
    def get_start_time_list(self):
        return [epi.get_start_time() for epi in self.schedule]
    
    def get_end_time_list(self):
        return [epi.get_end_time() for epi in self.schedule]
    

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
    
    def make_project(self):
        for episode in self.pre_schedule:
            self.schedule_episode(episode)
            ##プロジェクト内のエピソードが活動数に達したら終了
            if len(self.schedule) == self.__frequency:
                break
    


###検証      
                
RES = []

for i in range(1000):
    
    p = Project("all_all", 1)
    
#    print(p.get_frequency())
    
    pre = [x.output() for x in p.pre_schedule]
#    print(pre)
    
    pro = [x.output() for x in p.schedule]
    
    p.make_project()
    
    pro = [x.output() for x in p.schedule]
#    print(pro)
    a1 = -100000000000
    res = []
    for j in range(len(pro)):
        a2 = pro[j][0]
        res.append(a1 <= a2)
        a1 = pro[j][1]
    if len(res) != sum(res):
        print("error")
        break
    RES.extend(res)

print(len(RES) == sum(RES))





#
#a = 0
#
#b = 10
#
#c = -100
#d = 100
#
#print(not(d <= a or b <= c))

#class Schedule:
#    def __ init__(self):
#        self.__home = sample_home()
#        self.episodes = []
#        
#    def get_home():
#        return self.__home