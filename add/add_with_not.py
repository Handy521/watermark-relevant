#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 15:46:48 2019

@author: shinong
"""

import cv2
import numpy as np
# 加载图像
img1 = cv2.imread('286.jpg')
img2 = cv2.imread('55.png')
 
rows,cols,channels = img2.shape
roi = img1[0:rows, 0:cols ]
 
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)      # 将图片灰度化
ret, mask = cv2.threshold(img2gray, 150, 255, cv2.THRESH_BINARY)#ret是阈值（175）mask是二值化图像
mask_inv = cv2.bitwise_not(mask)#获取把logo的区域取反 按位运算
 
img1_bg = cv2.bitwise_and(roi,roi,mask=mask )#在img1上面，将logo区域和mask取与使值为0
 
# 取 roi 中与 mask_inv 中不为零的值对应的像素的值，其他值为 0 。
# 把logo放到图片当中
img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)#获取logo的像素信息
 
dst = cv2.add(img1_bg,img2_fg)#相加即可
img1[0:rows, 0:cols ] = dst
cv2.imshow('res',img1)
cv2.imshow('mask',mask)
cv2.imshow('mask_inv',mask_inv)
cv2.imshow('img_bg',img1_bg)
cv2.imshow('img_fg',img2_fg)
cv2.imshow('img_gray',img2gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
