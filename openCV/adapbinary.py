import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg',0)

dst = cv2.adaptiveThreshold(img,100,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY,3,0)
dst2 = cv2.adaptiveThreshold(img,100,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY,13,0)

cv2.imshow('img',img)
cv2.imshow('dst',dst)
cv2.imshow('dst2',dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# img：输入图像
# 100：最大值
# cv2.ADAPTIVE_THRESH_GAUSSIAN_C：自适应阈值算法，使用高斯加权求和
# cv2.THRESH_BINARY_INV：二值化类型，反转二值化
# 3：邻域大小
# 0：常数，从计算出的平均值或加权平均值中减去