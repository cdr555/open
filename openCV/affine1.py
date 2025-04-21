import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

# 获取图像的高度、宽度和通道数
h, w, ch = img.shape

#src定义源图像中的三个点,dst定义目标图像中的三个点
src = np.float32([[400,300],[800,300],[400,800]])
dst = np.float32([[500,400],[900,500],[600,900]])

M = cv2.getAffineTransform(src,dst)

new = cv2.warpAffine(img,M,(w,h))

cv2.imshow('img',img)
cv2.imshow('new',new)
cv2.waitKey(0)