# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:46:59 2018

@author: Yunfei
"""
from Robot import Robot
from Parser import Parser
from Calculator import Calculator

import time

if __name__ == '__main__':
    target_score = 100
    
    for i in range(target_score):
        print('[screen] begin')
        filename = Robot.getScreen(filename="p_"+str(i)+".png")
        print('[screen] processing')
        chess_point , target_point, t = Parser.getStartAndEndPoints(filename)
        print('[calculate] distance : start '+str(chess_point)+' end '+str(target_point))
        distance = Calculator.getDistance(chess_point, target_point)
        print('[calculate] time | distance '+str(distance))
        press_time = Calculator.getPressTime(distance)
        print('[jump] jump | time '+str(press_time))
        Robot.jump(int(press_time))
        print('[jump] ' + str(i) + ' success')
        time.sleep(press_time/1000 + 1)