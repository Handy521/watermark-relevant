#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 20:16:50 2018

@author: shinong
"""
import numpy as np
import cv2 
from matplotlib import pyplot as plt 
#queryImage = cv2.imread('grass2.jpg', 0) 
#trainingImage = cv2.imread('mask256.jpg', 0) 
#sift = cv2.xfeatures2d.SIFT_create() 
#kp1, des1 = sift.detectAndCompute(queryImage, None) 
#kp2, des2 = sift.detectAndCompute(trainingImage, None) 
#FLANN_INDEX_KDTREE = 0 
#indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5) 
#searchParams = dict(checks=50) 
#flann = cv2.FlannBasedMatcher(indexParams, searchParams) 
#matches = flann.knnMatch(des1, des2, k=2) 
#
#for i, (m, n) in enumerate(matches): 
#    if m.distance < 0.7 * n.distance: matchesMask[i] = [1, 0] 
#    drawParams = dict(matchColor=(0, 255, 0), 
#                      singlePointColor=(255, 0, 0), matchesMask=matchesMask, flags=0 ) 
#resultImage = cv2.drawMatchesKnn(queryImage, kp1, trainingImage, kp2, matches, None, **drawParams) 
#plt.xticks([]), plt.yticks([]) 
#plt.imshow(resultImage), plt.show() 
flag=0
a=[]
b=a
queryImage = cv2.imread('1275665242.jpg')
#queryImage=queryImage[0:393,200:700,0:3]
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(queryImage, None) 
trainImage = cv2.imread('mask256.jpg')
kp2, des2 = sift.detectAndCompute(trainImage, None)
FLANN_INDEX_KDTREE = 0 
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5) 
search_params = dict(checks=50) # or pass empty dictionary 
flann = cv2.FlannBasedMatcher(index_params, search_params) 
matches = flann.knnMatch(des1, des2, k=2) # 找出相匹配的特征点 
#for m, n in matches: 
#    if m.distance < 0.75 * n.distance:
#        x1 = kp1[m.queryIdx].pt[0] 
#        y1 = kp1[m.queryIdx].pt[1] 
#        x2 = kp2[m.trainIdx].pt[0] 
#        y2 = kp2[m.trainIdx].pt[1]#(x1,y1)he(x2,y2)is map point
#        a.append((x1,y1))
#        b.append((x2,y2))
#        flag+=1
matchesMask = [[0, 0] for i in range(len(matches))]         
for i, (m, n) in enumerate(matches): 
    if m.distance < 0.7* n.distance: matchesMask[i] = [1, 0] 
    drawParams = dict(matchColor=(0, 255, 0), 
                      singlePointColor=(100, 0, 0), matchesMask=matchesMask, flags=0 ) 
resultImage = cv2.drawMatchesKnn(queryImage, kp1, trainImage, kp2, matches, None, **drawParams) 
plt.xticks([]), plt.yticks([]) 
plt.imshow(resultImage), plt.show()        