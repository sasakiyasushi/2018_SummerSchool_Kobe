# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 10:50:06 2018

@author: sasaki
main_functions
"""


def make_project(project):
    for episode in project.pre_project:
        project.schedule_episode(episode)
        ##プロジェクト内のエピソードが活動数に達したら終了
        if len(project.project) == project.get_frequency():
            break
        

