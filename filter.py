import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

# # 定义卷积核
# kernel = np.ones((5,5),np.float32)/25

# # 应用卷积操作
# dst = cv2.filter2D(img, -1, kernel)

# 应用均值滤波
dst = cv2.blur(img,(5,5))

# 显示原始图像和处理后的图像
cv2.imshow('dst', dst)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
