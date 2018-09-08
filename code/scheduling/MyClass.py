# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:51:37 2018

@author: sasaki

クラスの定義
"""

##定数の読み込み
from CONSTANTS import SHIFT_LIMIT

##外部の関数読み込み
from func_activity_generation import sample_home, initial_sampling
#from func_mode_choice import mode_choice
#from func_dest_choice import dest_choice



class Episode:
    def __init__(self, start_time, duration):
        self.__INITIAL_START_TIME = start_time
        self.__INITIAL_DURATION = duration
        self.__start_time = start_time
        self.__duration = duration
        self.__place = -1
        self.__shift_direction = 1
        
    def get_start_time(self):
        return self.__start_time
    def get_duratein(self):
        return self.__duration
    def get_end_time(self):
        return self.__start_time + self.__duration
    def get_place(self):
        return self.__place
    def get_remain_shift(self):
        return self.__shift_direction * (SHIFT_LIMIT - abs(self.__INITIAL_START_TIME - self.__start_time))
    
    def set_place(self,p):
        self.__place = p
        
    def output(self):
        return self.__start_time, self.__duration



class Project:
    def __init__(self, category, purpose):
        self.__frequency, start_time_list, duration_list = initial_sampling(category, purpose)
        self.pre_project = [Episode(st,du) for st, du in zip(start_time_list, duration_list)]
        self.project = []
        
    def get_frequency(self):
        return self.__frequency
    
    def get_start_time_list(self):
        return [epi.get_start_time() for epi in self.project]
    
    def get_end_time_list(self):
        return [epi.get_end_time() for epi in self.project]

    def schedule_episode(self, new_episode):
        overlap_list = [] ## 新しく挿入するエピソードと時間の被りがあるエピソード
        prior_ind = -1 ## 新しく挿入するエピソードの前のエピソード
        for i, epi in enumerate(self.project):
            if epi.get_start_time() < new_episode.get_start_time():
                prior_ind = i ##開始時間が新しく挿入するエピソードより前の場合，indexを更新
            if not(new_episode.get_end_time() <= epi.get_start_time() or epi.get_end_time() <= new_episode.get_start_time()):
                overlap_list.append(i)
        overlap_num = len(overlap_list)
        if overlap_num == 0: ##時間的に被りがない場合，新しいエピソードを挿入
            self.project.insert(prior_ind+1, new_episode)
        elif overlap_num == 1:
            
        elif overlap_num == 2:
            
        else: ## 被りが三つ以上ある場合は，新しいエピソードが既存のエピソードを内包しているということなので排除
            pass
            
        
            
            
    
    def make_project(self):
        for episode in self.pre_project:
            self.schedule_episode(episode)
            ##プロジェクト内のエピソードが活動数に達したら終了
            if len(self.project) == self.__frequency:
                break
    
        

p = Project("all_all", 1)

pre = [x.output() for x in p.pre_project]
print(pre)

pro = [x.output() for x in p.project]
print(pro)

p.make_project()

pro = [x.output() for x in p.project]
print(pro)




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