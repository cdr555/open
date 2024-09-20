import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()

# 读取图像
a_path = '/Users/itlc00011/Desktop/rr/Test/a1.DNG'
b_path = '/Users/itlc00011/Desktop/rr/Test/a2.HEIC'
a = cv2.imread(a_path)

# 使用 PIL 读取 HEIC 图像
try:
    b_pil = Image.open(b_path)
    b = cv2.cvtColor(np.array(b_pil), cv2.COLOR_RGB2BGR)
except Exception as e:
    print(f"Error: Image at {b_path} did not load correctly. Exception: {e}")
    exit()

# 检查图像是否读取成功
if a is None:
    print(f"Error: Image at {a_path} did not load correctly.")
    exit()
if b is None:
    print(f"Error: Image at {b_path} did not load correctly.")
    exit()

# 调整 b 的尺寸和通道数以匹配 a
b_resized = cv2.resize(b, (a.shape[1], a.shape[0]))

# 确保通道数匹配
if a.shape[2] != b_resized.shape[2]:
    print("Error: The number of channels in the images do not match.")
    exit()

# 加权加法,将图像 a 的每个像素值乘以 1.2，图像 b_resized 的每个像素值乘以 1
# 然后将它们相加，并加上标量 0(加到结果图像上的标量值（可选，通常用于亮度调整))
c = cv2.addWeighted(a, 1.2, b_resized, 1, 0)

# 显示结果
cv2.namedWindow('ADD', cv2.WINDOW_NORMAL)
cv2.imshow('ADD', c)
cv2.waitKey(0)
cv2.destroyAllWindows()