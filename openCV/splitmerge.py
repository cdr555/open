import cv2
import numpy as np

# 创建一个空白图像
img = np.zeros((480, 640, 3), np.uint8)

# 分离图像通道
b, g, r = cv2.split(img)

# 修改蓝色和绿色通道的特定区域
b[10:100, 10:100] = 255
g[10:100, 10:100] = 255

# 合并图像通道
img2 = cv2.merge((b, g, r))

# 显示图像
cv2.imshow('img', img)
cv2.imshow('b', b)
cv2.imshow('g', g)
cv2.imshow('img2', img2)
key = cv2.waitKey(0)
if key & 0xFF == ord('q'):
    cv2.destroyAllWindows()