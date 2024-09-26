import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b3.png')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray.shape)

# 计算 Sobel 梯度
img1 = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
img2 = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# 计算 Harris 角点
img3 = cv2.cornerHarris(gray, 5, 3, 0.04)

# 扩展角点标记
img3 = cv2.dilate(img3, None)

# 设置阈值并标记角点
img[img3 > 0.5 * img3.max()] = [0, 0, 255]

# 显示结果
cv2.imshow('Harris Corners', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

