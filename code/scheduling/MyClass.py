# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 19:51:37 2018

@author: sasaki

クラスの定義
"""

##外部の関数読み込み
from func_activity_generation import sample_home, sample_frequency, sample_start_time, sample_duration, initialize_sampling
from func_mode_choice import mode_choice
from func_dest_choice import dest_choice



class Episode:
    def __ init__(self, start_time, duration):
        self.__start_time = start_time
        self.__duration = duration
        self.__place = -1
        
    def get_start_time():
        return self.__start_time
    def get_duratein():
        return self.__duration
    def get_end_time():
        return self.__start_time + self.__duration
    def get_place():
        return self.__place
    
    def set_place(p):
        self.__place = p



#class Project:
#    def __ init__(self):
#        self.episodes = []
#
#
#class Schedule:
#    def __ init__(self):
#        self.__home = sample_home()
#        self.episodes = []
#        
#    def get_home():
#        return self.__home