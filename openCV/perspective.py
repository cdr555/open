import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()

# 读取图像
a_path = '/Users/itlc00011/Desktop/rr/Test/a3.HEIC'

# 使用 PIL 读取 HEIC 图像
try:
    a_pil = Image.open(a_path)
    a = cv2.cvtColor(np.array(a_pil), cv2.COLOR_RGB2BGR)
except Exception as e:
    print(f"Error: Image at {a_path} did not load correctly. Exception: {e}")
    exit()

# 获取图像的高度、宽度和通道数
h, w, ch = a.shape

print(a.shape)

src = np.float32([[800,200],[4032,850],[250,3000],[4032,3200]])
dst = np.float32([[0,0],[4032,0],[0,3024],[4032,3024]])

M = cv2.getPerspectiveTransform(src,dst)

new = cv2.warpPerspective(a,M,(3000,4000))

cv2.imshow('img',a)
cv2.imshow('new',new)
cv2.waitKey(0)