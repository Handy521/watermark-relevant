#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 09:09:56 2018

@author: shinong
"""

import cv2
import numpy as np
def match_mask(src_photo,small_mask): #location    
    queryImage_1 = cv2.cvtColor(src_photo, cv2.COLOR_BGR2GRAY)    
#    trainImage = cv2.imread(mask_path,0)
    method = cv2.TM_CCOEFF # Apply template Matching 
    res = cv2.matchTemplate(queryImage_1, small_mask, method) 
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum 
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]: 
        x, y = min_loc 
    else: 
        x, y = max_loc        
    big_mask = np.zeros(queryImage_1.shape, np.uint8)
    big_mask[int(y):(int(y)+137),int(x):(int(x)+100)] = small_mask 
       
    return big_mask

def convert_whiteground(mask_photo):
    mask_new=255-mask_photo
    for row in range(mask_new.shape[0]):
        for col in range(mask_new.shape[1]):
            if mask_new[row,col]<250:
                mask_new[row,col]=128+mask_new[row,col]
    return mask_new
def convert_whiteground2(mask_photo):
    mask_160=255-mask_photo
    for row in range(mask_160.shape[0]):
        for col in range(mask_160.shape[1]):
            if mask_160[row,col]<250:
                mask_160[row,col]=160
    return mask_160
def convert_noboxbg(match_mask):
    for row in range(match_mask.shape[0]):
        for col in range(match_mask.shape[1]):
            if match_mask[row,col]>250:
                match_mask[row,col]=0
    return match_mask
def convert_noboxwhiteg(mask_new_1):
    for row in range(mask_new_1.shape[0]):
        for col in range(mask_new_1.shape[1]):
            if mask_new_1[row,col]>250:
                mask_new_1[row,col]=0
    mask_new_1=255-mask_new_1
    for row in range(mask_new_1.shape[0]):
        for col in range(mask_new_1.shape[1]):
            if mask_new_1[row,col]<250:
                mask_new_1[row,col]=160
    return mask_new_1
def convert_box(mask_new_2):
    kernel = cv2.getStructuringElement(1,(3*2+1,3*2+1))
    mask_new_2= cv2.dilate(mask_new_2 ,kernel) # dilate reduce box area,for match boundary
    for row in range(mask_new_2.shape[0]):
        for col in range(mask_new_2.shape[1]):
            if mask_new_2[row,col]>250:
                mask_new_2[row,col]=0       
    img=cv2.Canny(mask_new_2,200,300)        
    kernel = cv2.getStructuringElement(1,(1*2+1,1*2+1))
    mask_new_2= cv2.dilate(img ,kernel) # dilate for increase box boundary line weight         
    return mask_new_2

def color_neutral(src,maskphoto):
#    src = cv2.imread(srcphoto)
    save = np.zeros(src.shape, np.uint8) #创建一张空图像用于保存
    kernel = cv2.getStructuringElement(1,(1*2+1,1*2+1))
    maskphoto = cv2.dilate(maskphoto, kernel)#膨胀扩大白色区域面积
    for row in range(src.shape[0]):
        for col in range(src.shape[1]):
            for channel in range(src.shape[2]):
                if maskphoto[row, col] == 0:
                    val = 0                       
                else:
                    reverse_val = 255 - src[row, col, channel]
                    val = 255 - reverse_val * 256 /  maskphoto[row, col]
                    if val < 0: val = 0
                save[row, col, channel] = val
    return save
def inpaint(srcphoto,mask_blackphoto_1):
#    mask_blackphoto_1 = cv2.cvtColor(mask_blackphoto, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(1,(2*2+1,2*2+1))
    mask_blackphoto_1 = cv2.dilate(mask_blackphoto_1 ,kernel)
    
    dst = cv2.inpaint(srcphoto, mask_blackphoto_1, 3, cv2.INPAINT_TELEA)
    return dst
def crop_mask(mask_path):
    mask=cv2.imread(mask_path,0)
    small_mask=mask[0:137,69:169]
    return small_mask
def elimate_box(mask_template,src_photo):
    bigmask2=convert_whiteground2(mask_template)#创建一个白底背景然后框为反色的模板
    dst=color_neutral(src_photo,bigmask2)#反色中和
    bigmask3=convert_box(bigmask2)#创建框边缘，黑底
    dst2=inpaint(dst,bigmask3)#去除反色中和留下的边界框
    return dst2
def showGaussianBlurImage(srcImage,n):
    GaussianBlurImage = cv2.GaussianBlur(srcImage, (n * 2 + 1, n * 2 + 1), 0)  
    # 保证高斯滤波内核大小必须为正数或者奇数，不然会报错
    cv2.imshow("GaussianBlurImage", GaussianBlurImage)
def main():
    src='grass2.jpg'
    src_photo = cv2.imread(src)#读取待处理的原图
    #mask='mask256.jpg'
    #small_mask=cv2.imread(mask,0)
    mask_path= 'noground.jpg'
    small_mask=crop_mask(mask_path)   #剪切出小的模板
    mask_template=match_mask(src_photo,small_mask)#模板和大图进行匹配
    dst1=elimate_box(mask_template,src_photo)   #去除透明层
    bigmask0=convert_noboxbg(mask_template)#水印模板没有透明层
   
    dst2=inpaint(dst1,bigmask0)#图像修复
#    bigmask_white=convert_noboxwhiteg(mask_template)
#    dst4=color_neutral(src_photo,bigmask_white)
   
    cv2.imshow("desImage2", dst2)
    k=cv2.waitKey()  
    if k ==27:     # 键盘上Esc键的键值
        cv2.destroyAllWindows()   
    
#    cv2.imshow("mask", big_mask)
#cv2.imshow("mask0", bigmask0)
#cv2.imshow("mask_white", bigmask_white)
#cv2.imshow("mask2", bigmask2)
#cv2.imshow("mask3", bigmask3)
#cv2.imshow("desImage", dst)

if __name__=='__main__':
    main()












