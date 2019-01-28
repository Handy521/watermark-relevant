#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:50:17 2018

@author: shinong
"""

import cv2
import random

def saltimage(srcImage,num):
    for x in range(num):
        i=random.randint(0,srcImage.shape[0]-1)
        j=random.randint(0,srcImage.shape[1]-1)
        srcImage[i][j][0]=255
        srcImage[i][j][1]=255
        srcImage[i][j][2]=255
    return srcImage

def showboxFilterImage(n):
    boxFilterImage=cv2.boxFilter(srcImage,-1,(n+1,n+1))
    cv2.imshow("boxFilterImage",boxFilterImage)
    
def showblurImage(n):
    blurImage = cv2.blur(srcImage, (n + 1, n + 1))  # 加1是为了保证ksize不为(0,0)，不然会报错，因为Trackbar的取值范围是>=0
    cv2.imshow("blurImage", blurImage)
def showGaussianBlurImage(n):
    GaussianBlurImage = cv2.GaussianBlur(srcImage, (n * 2 + 1, n * 2 + 1), 0)  
    # 保证高斯滤波内核大小必须为正数或者奇数，不然会报错
    cv2.imshow("GaussianBlurImage", GaussianBlurImage)

def medianBlurImage(n):
	# 中值滤波能很好的处理掉椒盐点
    mediaImage = cv2.medianBlur(saltImage, n*2 + 1)
    # 保证中值滤波内核大小必须为>=1的奇数，不然会报错。
    cv2.imshow("medianBlurImage", mediaImage)

def bilateralFilterImage(n):
    bilateralImage = cv2.bilateralFilter(srcImage, n, n * 2, n / 2)
    cv2.imshow("bilateralFilterImage", bilateralImage)
def custom_blur_demo(image):
  kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32) #锐化
  dst = cv.filter2D(image, -1, kernel=kernel)
   
srcImage1 = cv2.imread("/home/shinong/桌面/img_blur.png")
srcImage=srcImage1[240:408,115:460]
cv2.imshow("srcImage", srcImage)
value = 3                               # 初始化bar的位置
saltImage = srcImage.copy() 
#saltImage = saltimage(saltImage, 3000)  # 生成3000个点，做椒盐效果
#cv2.imshow("saltImage", saltImage)

cv2.namedWindow("boxFilterImage")
cv2.createTrackbar("ksize", "boxFilterImage", value, 40, showboxFilterImage)
boxFilterImage = cv2.boxFilter(srcImage, -1, (value + 1, value + 1))
cv2.imshow("boxFilterImage", boxFilterImage)

cv2.namedWindow("blurImage")
cv2.createTrackbar("ksize", "blurImage", value, 40, showblurImage)
blurImage = cv2.blur(srcImage, (value + 1, value + 1))
cv2.imshow("blurImage", blurImage)

cv2.namedWindow("GaussianBlurImage")
cv2.createTrackbar("ksize", "GaussianBlurImage", value, 40, showGaussianBlurImage)
GaussianBlurImage = cv2.GaussianBlur(srcImage, (value * 2 + 1, value * 2 + 1), 0)  # 保证高斯滤波内核大小必须为正数
cv2.imshow("GaussianBlurImage", GaussianBlurImage)

cv2.namedWindow("medianBlurImage")
cv2.createTrackbar("ksize", "medianBlurImage", value, 40, medianBlurImage)
mediaImage = cv2.medianBlur(saltImage, value)
cv2.imshow("medianBlurImage", mediaImage)

cv2.namedWindow("bilateralFilterImage")
cv2.createTrackbar("ksize", "bilateralFilterImage", value, 40, bilateralFilterImage)

bilateralImage = cv2.bilateralFilter(srcImage, value, value * 2, value / 2)
cv2.imshow("bilateralFilterImage", bilateralImage)
k=cv2.waitKey()  
if k ==27:     # 键盘上Esc键的键值
   cv2.destroyAllWindows()   









    