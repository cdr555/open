import cv2
import numpy as np
from PIL import Image
import pillow_heif

# 注册 HEIF 插件
pillow_heif.register_heif_opener()

def stitch_images(a, b):
    # 转换为灰度图像
    gray1 = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

    # 使用 SIFT 检测关键点和描述符
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # 使用 BFMatcher 进行特征匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # 应用比值测试来筛选匹配
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append((m.queryIdx, m.trainIdx))

    # 提取匹配的关键点
    src_pts = np.float32([keypoints1[i].pt for i, _ in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[i].pt for _, i in good]).reshape(-1, 1, 2)

    # 使用 RANSAC 估计单应性矩阵
    H, status = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 2.0)

    # # 使用单应性矩阵进行图像变换
    # height, width = a.shape[:2]
    # result = cv2.warpPerspective(b, H, (width + b.shape[1], height))

    # # 将第一张图像放置在结果图像的左上角
    # result[0:height, 0:width] = a
    result = cv2.warpPerspective(b, H, (a.shape[1] + b.shape[1], a.shape[0]))
    result[0:a.shape[0], 0:a.shape[1]] = a

    return result

# 读取图像
# img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1184.jpg')
# img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1185.jpg')
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

# 拼接图像
result = stitch_images(a, b)

# 显示结果
cv2.imshow('Stitched Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()