#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 11:25:57 2018

@author: shinong
"""

import cv2 
import numpy as np 
srcImage = cv2.imread("piexlvalue160.jpg") 
print(srcImage.shape) 
print(srcImage[0][0][0]) 
print(srcImage[0][1][0]) 
print(srcImage[0][2][0]) 
print(srcImage[0][3][0]) 
print(srcImage[0][4][0]) 
print(srcImage[:10, :5, 0]) 
(B, G, R) = cv2.split(srcImage) # 分离元原图像通道，得到单通道灰度图像，为灰白色 
print(B.shape) 
print(B[0][0]) 
cv2.imshow("srcImage", srcImage) 
cv2.imshow("B", B) # 灰度图，灰白色 
cv2.imshow("G", G) # 灰度图，灰白色 
cv2.imshow("R", R) # 灰度图，灰白色 
print(type(B[0][0])) # 验证数据类型，为下面构建值为0的矩阵做条件 
zeros = np.zeros(srcImage.shape[:2], dtype=np.uint8) # 值为0矩阵，为了与B、G、R合并， 
print(type(zeros[0][0])) # 验证构建矩阵数据类型 
B[:100]=0 # 分离后的通道，操作时，并不影响原图像 
B_new = cv2.merge((B, zeros, zeros)) # 颜色通道合并，得到B色图像，将G、R值填充为0。三通道图像，蓝色 
G_new = cv2.merge([zeros, G, zeros]) # 颜色通道合并，得到G色图像，将B、R值填充为0。三通道图像，绿色 
R_new = cv2.merge([zeros, zeros, R]) # 颜色通道合并，得到R色图像，将B、G值填充为0。三通道图像，红色 srcImage = cv2.merge((B, G, R)) # 分离后的通道，操作后，重新合并为原图像，才能达到修改原图像的作用 
print(B_new.shape) 
print(G_new.shape) 
print(R_new.shape) 
cv2.imshow("srcImage1", srcImage) 
cv2.imshow("B_new", B_new) 
cv2.imshow("G_new", G_new) 
cv2.imshow("R_new", R_new) 
cv2.waitKey(0)
