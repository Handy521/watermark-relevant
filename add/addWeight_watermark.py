#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 09:41:28 2019

@author: shinong
"""

import numpy as np
import cv2 
from math import * 
#################
def rotate(img):
    height,width=img.shape[:2] 
    a=[-1,1]
    flag=np.random.choice(a)
    degree=45*flag #旋转
    heightNew=int(width*fabs(sin(radians(degree)))+height*fabs(cos(radians(degree)))) 
    widthNew=int(height*fabs(sin(radians(degree)))+width*fabs(cos(radians(degree)))) 
    matRotation=cv2.getRotationMatrix2D((width/2,height/2),degree,1)   
    matRotation[0,2] +=(widthNew-width)/2  #重点在这步
    matRotation[1,2] +=(heightNew-height)/2  #重点在这步
    
    imgRotation=cv2.warpAffine(img,matRotation,(widthNew,heightNew),borderValue=(0,0,0)) #piexl value
    return imgRotation
def add_small_watermark(src):
    mask=cv2.imread('mask_rr.png')
    if min(src.shape[:2])<800:
        mask=cv2.resize(mask,(int(mask.shape[1]*0.5),int(mask.shape[0]*0.5)))
    mask_init= np.zeros(src.shape, np.uint8)
    mask_init[0:mask.shape[0],30:mask.shape[1]+30]=mask
    img1=cv2.addWeighted(src,0.95,mask_init,0.4,0)
    return img1
def add_medium_watermark(src2): 
    mask1=cv2.imread('mask_m_shinbk.jpg')
    mask1=rotate(mask1)#755*755
    mask_init2=np.zeros(src2.shape, np.uint8)#must re_init
    
    y1,x1=mask_init2.shape[:2]
    if min(y1,x1)<755:
        mask1=cv2.resize(mask1,(int(mask1.shape[1]*0.8),int(mask1.shape[0]*0.8)))
    y,x=mask1.shape[:2]   
    yy,xx=int((y1/2-y/2)),int((x1/2-x/2))
    try:
        mask_init2[yy:int((y1/2+y/2)),xx:int((x1/2+x/2))]=mask1
    except:
        mask_init2=mask_init2
    img2=cv2.addWeighted(src2,1,mask_init2,0.1,0)
    return img2

src=cv2.imread('leaf.jpg') #
img1=add_small_watermark(src)
img2=add_medium_watermark(img1) 


cv2.imshow('img2',img2)  

#cv2.imwrite('img_f0.1sf.png',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
