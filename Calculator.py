# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:40:02 2018

@author: Yunfei
"""

class Calculator:
    
    def getDistance(start, end):
        return ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
    
    def getPressTime(distance, height=1280):
        multi = 1
        if(height != 1280):
            multi = 2560 / height
        return distance * 2.099 * multi
        