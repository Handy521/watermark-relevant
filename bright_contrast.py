#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 18:21:21 2018

@author: shinong
"""

import cv2 
import numpy as np 
gcontrastvalue = 80 # 对比度 
gbrightvalue = 80 # 亮度 
def contrast(contrastvalue): 
    desImage = srcImage.copy() 
    global gcontrastvalue 
    global gbrightvalue 
    print('gcontrastvalue：', gcontrastvalue) 
    print('gbrightvalue：', gbrightvalue) 
    table = [] 
    for i in range(256): 
        data = int(i * gcontrastvalue * 0.01 + gbrightvalue) 
        if data < 0: 
            table.append(0) 
        elif data > 255: 
            table.append(255) 
        else: 
            table.append(data) 
    table = np.array(table, dtype=np.uint8) # 将数组转换为映射矩阵，数据类型与原图像数据保持一致 
    cv2.LUT(srcImage, table, desImage) # 利用系统函数LUT进行映射矩阵替换原图形数据 
    cv2.imshow("window1", desImage) 
    gcontrastvalue = contrastvalue 
def bright(brightvalue): 
    desImage = srcImage.copy() 
    global gcontrastvalue 
    global gbrightvalue 
    print('gcontrastvalue：', gcontrastvalue) 
    print('gbrightvalue：', gbrightvalue) 
    table = [] 
    for i in range(256): 
        data = int(i * gcontrastvalue * 0.01 + gbrightvalue) 
        if data < 0: 
            table.append(0) 
        elif data > 255: 
            table.append(255) 
        else: 
            table.append(data) 
    table = np.array(table, dtype=np.uint8) # 将数组转换为映射矩阵，数据类型与原图像数据保持一致 
    cv2.LUT(srcImage, table, desImage) # 利用系统函数LUT进行映射矩阵替换原图形数据 
    cv2.imshow("window1", desImage) 
    gbrightvalue = brightvalue 
srcImage = cv2.imread("open.png") 
# print(srcImage.shape)             # 获取原图像的尺寸 
# print(type(srcImage[0][0][0]))    # 获取原图像的数据类型，为后面做映射矩阵服务 
cv2.namedWindow("window1") 
cv2.createTrackbar("contrast", "window1", 80, 300, contrast) 
cv2.createTrackbar("brightness", "window1", 80, 100, bright) 
cv2.imshow("window1", srcImage) 
k=cv2.waitKey()  
if k ==27:     # 键盘上Esc键的键值
   cv2.destroyAllWindows()  
