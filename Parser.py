# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 19:33:46 2018

@author: Yunfei
"""
from PIL import Image
import matplotlib.pyplot as plt #plt 用于显示图片
import matplotlib.image as mpimg #mpimg 用于读取图片
import numpy as np

class Parser:
    
    score_bottom = 192
    
    chess_color = (55,57,98,255)
    
    def distance(bg,pixel,p=0.02):
        s = 0
        for i in range(len(pixel)):
            s = s + (pixel[i]/255 - bg[i]/255)**2
        if(s > p):
            return False
        return True
    
    def eq(a,b,p):
        return a == b
    
    def getStartAndEndPoints(filename, debug=False):
        
        step = 3
        
        img = Image.open(filename)
        bg = img.getpixel((0,0)) #背景颜色
    
        box_color = None #目标棋盘的颜色   
        
        target = { #目标棋盘的坐标
            'top':[-1,-1],
            'left':[-1,-1],
            'bottom':[-1,-1],
            'right':[-1,-1]    
        }
        
        chess_point = [-1,-1]
        
        left_fix = False
        right_fix = False
        bottom_fix = False
    
        for y in range(Parser.score_bottom, int(img.height*2/3),2):
            
            border = [-1,-1] # (start,end)
            
            chess_border = [-1,-1]
            
            #扫描每一列
            for x in range(0, img.width, step):
                pixel = img.getpixel((x,y))
                
                bg_sim = Parser.distance(bg,pixel,0.005)
                if(bg_sim):
                    bg = pixel
                    continue
                
                if(Parser.distance(Parser.chess_color,pixel,0.1)):
                    #找棋子的坐标
                    if(Parser.distance(Parser.chess_color, pixel,0.005)):
                        if(chess_border[0] == -1):
                            chess_border[0] = x
                            chess_border[1] = x
                        else:
                            chess_border[1] = x
                    continue
                
                #和背景、棋子的颜色不同
                if(box_color == None):
                    box_color = pixel
                    print(box_color)
                    
                #目标盒子的坐标
                if(Parser.distance(box_color,pixel,0.001)):
                    if(border[0] == -1):
                        border[0] = x
                        border[1] = x
                    else:
                        border[1] = x
                
            
            if(chess_border[0] != -1):
                chess_point = [(chess_border[0] + chess_border[1])/2, y]    
                continue
                                
            if(border[0] == -1):
                continue
            
            if(target['top'] == [-1,-1]):
                target['top'] = [(border[0]+border[1])/2,y]
                continue
            
            if(target['left'] == [-1,-1]):
                target['left'] = [border[0],y]
                target['right'] = [border[1],y]
                continue
            if(target['left'][0] > border[0] and (not left_fix)):
                target['left'] = [border[0],y]
            else:
                left_fix = True
            if(target['right'][0] < border[1] and (not right_fix)):
                target['right'] = [border[1],y]
            else:
                right_fix = True
            
            if(not bottom_fix):
                target['bottom'] = [(border[0]+border[1])/2,y]
            
            if(target['bottom'] != [-1,-1] and (not bottom_fix) and border[0] == -1):
                bottom_fix = True
                
        print(target)
        #差错检验
        try:
            center = [-1,-1]
            if(target['left'][1] == -1 or target['left'][0] == -1):
                if(target['right'][0] == -1 or target['right'][1] == -1):
                    target['left'] = [target['top'][0], target['top'][1] + 30]
                    target['right'] = target['left']
                else:
                    target['left'] = target['right']
    
            if(target['bottom'][0] < target['left'][0] or target['bottom'][0] > target['right'][0]):
                target['bottom'][0] = target['top'][0]
                
            center[0] = (target['top'][0] + target['bottom'][0])/2
            center[1] = (target['left'][1] + target['right'][1])/2
        except:
            print('center calculate err: ',target)
        finally:
            Parser.draw(chess_point,center,filename,target)
        
        return chess_point, center, target
    
    def revise(target):
        left = True
        #差错检验
        if((target['top'][0] - target['left'][0]) > (target['right'][0] - target['top'][0])):
            target['left'][0] = 2*target['top'][0] - target['right'][0]
            left = False
        else:
            target['right'][0] = 2*target['top'][0] - target['left'][0]
        
        if((target['right'][1] - target['top'][1]) < (target['bottom'][1] - target['right'][0])):
            t = 'right'
            if(left):
                t = 'left'
            target['bottom'][1] = 2*target[t][1] - target['top'][1]
#                else:
#                    target['top'][1] = 2*target['right'][1] - target['bottom'][1]
            
        center = [-1,-1]
        center[0] = (target['left'][0] + target['right'][0])/2
        center[1] = (target['top'][1] + target['bottom'][1])/2
        return center
            
    def draw(chess_point, center, filename, target=None):           
        lena = mpimg.imread(filename) #读取和代码处于同一目录下的lena.png
        plt.figure(num=1,figsize=(15,9))
        plt.imshow(lena) # 显示图片
        if(center != None):
            plt.scatter(center[0],center[1],color='b')
        plt.scatter(chess_point[0],chess_point[1],color='g')
        if(target != None):
            plt.scatter(target['top'][0],target['top'][1], color='r', marker='o')
            plt.scatter(target['left'][0],target['left'][1], color='r', marker='*')
            plt.scatter(target['right'][0],target['right'][1], color='r', marker='+')
            plt.scatter(target['bottom'][0],target['bottom'][1], color='r', marker='.')
        plt.show()
        
if __name__ == '__main__':
    filename = 'screen/p_0.png'
    chess_point, center, target = Parser.getStartAndEndPoints(filename)
    Parser.draw(chess_point,center,filename,target)