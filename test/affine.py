import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

# 获取图像的高度、宽度和通道数
h, w, ch = img.shape

# 定义仿射变换矩阵,a & b & tx \ c & d & ty
# a = 1 和 d = 1：表示没有缩放
# b = 0 和 c = 0：表示没有旋转和剪切
# tx = 500：表示在 x 方向平移 500 像素
# ty = 300：表示在 y 方向平移 300 像素

M = np.float32([[1, 0, 500], [0, 1, 300]])

# 中心点,旋转角度(逆时针),缩放比例
M = cv2.getRotationMatrix2D((100,100),20,0.8)

# 应用仿射变换,(输出图像的尺寸,宽度为 w,高度为 h)
new = cv2.warpAffine(img, M, (int(w/2), int(h/2)))

print(new.shape)

# 显示原始图像和变换后的图像
cv2.imshow('img', img)
cv2.imshow('new', new)

# 等待按键事件
cv2.waitKey(0)