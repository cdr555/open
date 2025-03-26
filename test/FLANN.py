import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()

# 读取图像
a_path = '/Users/itlc00011/Desktop/rr/Test/left.heic'
b_path = '/Users/itlc00011/Desktop/rr/Test/right.heic'

# 使用 PIL 读取图像
try:
    a_pil = Image.open(a_path)
    a = cv2.cvtColor(np.array(a_pil), cv2.COLOR_RGB2BGR)
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

# 转换为灰度图像
gray1 = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

# 创建特征检测器
sift = cv2.SIFT_create()

# 计算特征点与描述子
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# 创建匹配器
index_params = dict(algorithm=1, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# 特征匹配
matches = flann.knnMatch(des1, des2, k=2)

# 遍历每个匹配对 m, n，筛选符合的进入 good[]
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])

# 绘制匹配点
if len(good) > 4:
    srcPts = np.float32([kp1[m[0].queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dstPts = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1, 1, 2)
    
    # 计算单应性矩阵
    H, _ = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)
    
    h, w = a.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, H)
    img2 = cv2.polylines(b, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good), 4))
    matchesMask = None
    exit()

img3 = cv2.drawMatchesKnn(a, kp1, img2, kp2, good, None, flags=2)
cv2.imshow('matches', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
