import numpy as np
import cv2


_DILATE_KERNEL = np.array([[0, 0, 1, 0, 0],
                           [0, 1, 1, 1, 0],
                           [1, 1, 1, 1, 1],
                           [0, 1, 1, 1, 0],
                           [0, 0, 1, 0, 0]], dtype=np.uint8)

class WatermarkRemover(object):
    """"
    去除图片中的水印(Remove Watermark)
    """

    def __init__(self, mask_path):
        self.watermark_template_gray_img = None
        self.watermark_template_mask_img = None
        self.watermark_template_h = 0
        self.watermark_template_w = 0
        self.watermark_start_x = 0
        self.watermark_start_y = 0
        # 切换核函数
        self.kernel = cv2.getStructuringElement(cv2.MORPH_DILATE, (5, 5))
#         self.kernel = _DILATE_KERNEL
        self.load_watermark_template(mask_path)
    
    def dilate(self, img):
        """
        对图片进行膨胀计算
        :param img:
        :return:
        """
        dilated = cv2.dilate(img, _DILATE_KERNEL)
        return dilated

    def load_watermark_template(self, watermark_template_filename):
        """
        处理水印模板，生成对应的检索位图和掩码位图
        检索位图
            即处理后的灰度图，去除了非文字部分

        :param watermark_template_filename: 水印模板图片文件名称
        :return: x1, y1, x2, y2
        """
        # 水印模板原图
        img = cv2.imread(watermark_template_filename)

        # 灰度图、掩码图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        mask = self.dilate(mask)  # 使得掩码膨胀一圈，以免留下边缘没有被修复

        # 水印模板原图去除非文字部分
        img = cv2.bitwise_and(img, img, mask=mask)

        # 后面修图时需要用到三个通道
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        self.watermark_template_gray_img = gray
        self.watermark_template_mask_img = mask

        self.watermark_template_h = img.shape[0]
        self.watermark_template_w = img.shape[1]

        return gray, mask

    def find_watermark_from_gray(self, gray_img):
        """
        从原图的灰度图中寻找水印位置
        :param gray_img: 原图的灰度图
        :param watermark_template_gray_img: 水印模板的灰度图
        :return: x1, y1, x2, y2
        """
        method = cv2.TM_CCOEFF
        # Apply template Matching
        res = cv2.matchTemplate(gray_img, self.watermark_template_gray_img, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            x, y = min_loc
        else:
            x, y = max_loc

        return x, y, x + self.watermark_template_w, y + self.watermark_template_h
   
    def convert_noboxbg(self, match_mask):
        """
        转换为无box背景
        """
        match_mask = np.where(match_mask > 250, 0, match_mask)
        
        return match_mask


    
    def match_mask_template(self, img):
        """
        使用水印和原图进行匹配
        """
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
        res = cv2.matchTemplate(img_gray, self.watermark_template_gray_img, cv2.TM_CCOEFF)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum 
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        x, y = max_loc        
        mask_template = np.zeros(img_gray.shape, np.uint8)
        mask_template[int(y):(int(y)+self.watermark_template_h),int(x):(int(x)+self.watermark_template_w)] = self.watermark_template_gray_img 
    
        return mask_template
    
    def convert_whiteground(self, img):
        """
        创建一个白底背景然后框为反色的模板
        """
        img = 255 - img
        img = np.where(img < 250, 160, img)
        return img

    
    def color_neutral(self, src, mask_template):
        """
        反色中和?
        """
        save = np.zeros(src.shape, np.uint8) #创建一张空图像用于保存
        mask_template = cv2.dilate(mask_template, self.kernel)#膨胀扩大白色区域面积
        for row in range(src.shape[0]):
            for col in range(src.shape[1]):
                for channel in range(src.shape[2]):
                    if mask_template[row, col] == 0:
                        val = 0                       
                    else:
                        reverse_val = 255 - src[row, col, channel]
                        val = 255 - reverse_val * 256 /  mask_template[row, col]
                        if val < 0: val = 0
                    save[row, col, channel] = val
        return save
    
    def convert_box(self, mask_template):
        """
        创建框边缘，黑底
        """
        mask_template= cv2.dilate(mask_template , self.kernel) # dilate reduce box area,for match boundary
        mask_template = np.where(mask_template > 250, 0, mask_template)   
        img = cv2.Canny(mask_template, 200, 300)        
        mask_template= cv2.dilate(img, self.kernel) # dilate for increase box boundary line weight         
        
        return mask_template
    
    def remove_mongolia_raw(self, img, mask_template):
        """
        去除图像的蒙层
        """
        mask_template = self.convert_whiteground(mask_template) # 水印模板没有透明层
        tmp_img = self.color_neutral(img, mask_template) # 反色中和
        mask_template = self.convert_box(mask_template) # 创建框边缘，黑底
        mask_template = cv2.dilate(mask_template, self.kernel)
        ret = cv2.inpaint(tmp_img, mask_template, 3, cv2.INPAINT_TELEA)
        return ret
    
    def remove_watermark_raw(self, img, mask_template):
        """
        去除图片中的水印
        :param img: 待去除水印图片位图
        :param watermark_template_gray_img: 水印模板的灰度图片位图，用于确定水印位置
        :param watermark_template_mask_img: 水印模板的掩码图片位图，用于修复原始图片
        :return: 去除水印后的图片位图
        """
        mask_template = self.convert_noboxbg(mask_template)
        mask_template = cv2.dilate(mask_template, self.kernel)
        ret_img = cv2.inpaint(img, mask_template, 3, cv2.INPAINT_TELEA)
        
        return ret_img     
    
    def remove_watermark(self, filename, output_filename=None):
        """
        去除图片中的水印
        :param filename: 待去除水印图片文件名称
        :param output_filename: 去除水印图片后的输出文件名称
        :return: 去除水印后的图片位图
        """
        img = cv2.imread(filename)
        mask_template = self.match_mask_template(img)
        # 1. 去除蒙层
        img_remove_mongolia = self.remove_mongolia_raw(img, mask_template)
        # 2. 去除水印
        img_remove_water_mask = self.remove_watermark_raw(img_remove_mongolia, mask_template)
        if output_filename:
            cv2.imwrite(output_filename, img_remove_water_mask)
            
        return img_remove_water_mask


def main():
	watermark_template_filename = 'data/mask.jpg'
	remover = WatermarkRemover(watermark_template_filename)
	remover.remove_watermark('data/1.jpg', 'out.jpg')


if __name__ == '__main__':
	main()

