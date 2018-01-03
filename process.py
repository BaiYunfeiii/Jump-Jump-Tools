# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 12:46:23 2018

@author: Yunfei
"""

from PIL import Image

score = {
    'bottom' : 192
}

chess_color = (55,57,98,255)

filename = 'screen/p_19.png'

def sim(bg,pixel,p=0.1):
    s = 0
    for i in range(len(pixel)):
        s = s + (pixel[i]/255 - bg[i]/255)**2
    if(s > p):
        return False
    return True
    

with open(filename,'rb') as f:
    img = Image.open(f)
    bg = img.getpixel((0,0)) #背景颜色

    box_color = None #目标棋盘的颜色   
    
    target = { #目标棋盘的坐标
        'top':[],
        'left':[],
        'bottom':[],
        'right':[]    
    }
    
    chess_point = [-1,-1]

    leftSetted = False;    
    
    max_width = 0; # 目标棋盘的宽度
    
    firstMatch_y = True
    
    #扫描每一行
    last_border = [0,0]
    for y in range(score['bottom'], img.height):
        
        border = [-1,-1] # (start,end)
        firstMatch_x = True
        
        chess_border = [-1,-1]
        
        #扫描每一列
        for x in range(img.width):
            pixel = img.getpixel((x,y))
            
            if(box_color == None and (not sim(bg,pixel))):
                box_color = pixel
                
            #目标盒子的坐标
            if(box_color == pixel):
                if(border[0] == -1):
                    border[0] = x
                    border[1] = x
                else:
                    border[1] = x
            
            #找棋子的坐标
            if(sim(chess_color, pixel,0.005)):
                if(chess_border[0] == -1):
                    chess_border[0] = x
                    chess_border[1] = x
                else:
                    chess_border[1] = x
        
        if(chess_border[0] != -1):
            chess_point = [(chess_border[0] + chess_border[1])/2, y]           
                            
        if(border[0] == -1):
            continue
        
        if(target['top'] == []):
            target['top'] = [(border[0]+border[1])/2,y]
            continue
        
        if(target['left'] == []):
            target['left'] = [border[0],y]
            target['right'] = [border[1],y]
            continue
        elif(target['left'][0] > border[0]):
            target['left'] = [border[0],y]
        elif(target['right'][0] < border[1]):
            target['right'] = [border[1],y]
            
        target['bottom'] = [(border[0]+border[1])/2,y]
    
    #差错检验
    if((target['top'][0] - target['left'][0]) > (target['right'][0] - target['top'][0])):
        target['left'][0] = 2*target['top'][0] - target['right'][0]
    else:
        target['right'][0] = 2*target['top'][0] - target['left'][0]
    
    if((target['right'][1] - target['top'][1]) < (target['bottom'][1] - target['right'][0])):
        target['bottom'][1] = 2*target['right'][1] - target['top'][1]
    else:
        target['top'][1] = 2*target['right'][1] - target['bottom'][1]
        
    center = [-1,-1]
    center[0] = (target['left'][0] + target['right'][0])/2
    center[1] = (target['top'][1] + target['bottom'][1])/2
    
    import matplotlib.pyplot as plt #plt 用于显示图片
    import matplotlib.image as mpimg #mpimg 用于读取图片
    import numpy as np
    
    lena = mpimg.imread(filename) #读取和代码处于同一目录下的lena.png
    plt.figure(num=1,figsize=(30,18))
    plt.imshow(lena) # 显示图片
    plt.scatter(center[0],center[1],color='b')
    plt.scatter(chess_point[0],chess_point[1],color='g')
    plt.show()