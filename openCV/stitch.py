import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()

# 读取图像
# a = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1184.jpg')
# b = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1185.jpg')// false

a_path = '/Users/itlc00011/Desktop/rr/Test/left.heic'
b_path = '/Users/itlc00011/Desktop/rr/Test/right.heic'
try:
    a_pil = Image.open(a_path)
    a = cv2.cvtColor(np.array(a_pil), cv2.COLOR_RGB2BGR)
    b_pil = Image.open(b_path)
    b = cv2.cvtColor(np.array(b_pil), cv2.COLOR_RGB2BGR)
except Exception as e:
    print(f"Error: Image at {b_path} did not load correctly. Exception: {e}")
    exit()


# 转换为灰度图像
gray1 = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

# 使用 SIFT 检测关键点和描述符
sift = cv2.SIFT_create()

k1, d1 = sift.detectAndCompute(gray1, None)
k2, d2 = sift.detectAndCompute(gray2, None)
# print(d1.shape)

# 使用 BFMatcher 进行特征匹配
bf = cv2.BFMatcher()

matches = bf.knnMatch(d1, d2, 2)
# print(matches)


good = []
for m, n in matches:
    if m.distance < 0.8 * n.distance:
        good.append((m.queryIdx, m.trainIdx))

# 提取匹配点x,y坐标        
k1 = np.float32([kp.pt for kp in k1])
k2 = np.float32([kp.pt for kp in k2])

# 求出可靠匹配x,y坐标
k1 = np.float32([k1[i[0]] for i in good]).reshape(-1, 1, 2)
k2 = np.float32([k2[i[1]] for i in good]).reshape(-1, 1, 2)

M,status = cv2.findHomography(k2, k1, cv2.RANSAC, 5.0)
# print(M)
 # 拼接图像
result = cv2.warpPerspective(b, M, (a.shape[1] + b.shape[1], a.shape[0]))
result[0:a.shape[0], 0:a.shape[1]] = a

# 显示结果
cv2.imshow('Stitched Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()