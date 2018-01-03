# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:48:51 2018

@author: Yunfei
"""
import os
import random

class Robot:
    
    def jump(press_time, w=720, h=1280):
        left = int(w / 2)
        top = int(1584 * (h / 1920.0))
        left = int(random.uniform(left-50, left+50))
        top = int(random.uniform(top-10, top+10))    # 随机防 ban
        swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, left, top
        cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
            x1=swipe_x1,
            y1=swipe_y1,
            x2=swipe_x2,
            y2=swipe_y2,
            duration=press_time
        )
        os.system(cmd)
        
    def getScreen(filename='screen.png'):
        os.system("adb shell screencap -p /sdcard/screen.png")
        os.system("adb pull /sdcard/screen.png screen/"+filename)
        return 'screen/'+filename