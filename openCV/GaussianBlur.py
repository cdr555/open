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

# 读取图像
# img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/a5.bmp')

# 应用高斯模糊
# dst = cv2.GaussianBlur(img, (3, 3), sigmaX=1,sigmaY=1)

# 应用中值滤波
# dst = cv2.medianBlur(img,9)

# 应用双边滤波
dst = cv2.bilateralFilter(img,15,75,75)

# 显示原始图像和处理后的图像
cv2.imshow('dst', dst)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()