import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()
b_path = '/Users/itlc00011/Desktop/rr/Test/a6.HEIC'

# 使用 PIL 读取 HEIC 图像
try:
    b_pil = Image.open(b_path)
    img = cv2.cvtColor(np.array(b_pil), cv2.COLOR_RGB2BGR)
except Exception as e:
    print(f"Error: Image at {b_path} did not load correctly. Exception: {e}")
    exit()

# 应用Sobel 算子
d1 = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
d2 = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)

# 应用Laplacion 算子
#d3 = cv2.Laplacian(img,cv2.CV_64F,ksize=5)

# 合并Sobel 结果
dst = cv2.add(d1 , d2)

cv2.imshow('img',img)
cv2.imshow('d1',d1)
cv2.imshow('d2',d2)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
