import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b2.png', 0)

# 定义腐蚀操作的核
# kernel = np.zeros((11, 11), np.uint8)
# print(kernel)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
print(kernel)

# # 应用腐蚀操作
# dst = cv2.erode(img, kernel, iterations=1)

# # 应用膨胀操作
# dst2 = cv2.dilate(img,kernel,1)

# 开运算
# dst = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

# 梯度
# dst = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)

# 顶帽运算
# dst = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)

# 黑帽运算
dst = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)


# 显示原始图像和处理后的图像
cv2.imshow('img', img)
cv2.imshow('dst', dst)
# cv2.imshow('dst2', dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()