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

# img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1184.jpg')
# img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1185.jpg')
# img1 = cv2.resize(img1, (4000, 6048))
# img2 = cv2.resize(img2, (4000, 6048))

def stitch_images(a, b, H):
    rows1, cols1 = a.shape[:2]
    rows2, cols2 = b.shape[:2]

    list_of_points_1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)

    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

    translation_dist = [-x_min, -y_min]

    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(b, H_translation.dot(H), (x_max - x_min, y_max - y_min))
    output_img[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = a

    return output_img

def get_homo(a, b):
    gray1 = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()

    k1, d1 = sift.detectAndCompute(gray1, None)
    k2, d2 = sift.detectAndCompute(gray2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(d1, d2, k=2)

    verify_ratio = []

    for m1, m2 in matches:
        if m1.distance < 0.75 * m2.distance:
            verify_ratio.append(m1)

    min_matches = 8
    if len(verify_ratio) > min_matches:
        gray1_pts = []
        gray2_pts = []

        for m in verify_ratio:
            gray1_pts.append(k1[m.queryIdx].pt)
            gray2_pts.append(k2[m.trainIdx].pt)

        gray1_pts = np.float32(gray1_pts).reshape(-1, 1, 2)
        gray2_pts = np.float32(gray2_pts).reshape(-1, 1, 2)

        H, mask = cv2.findHomography(gray1_pts, gray2_pts, cv2.RANSAC, 5.0)
        return H
    else:
        print('err:no enough matches')
        exit()

imputs = np.hstack((a, b))

H = get_homo(a, b)

result_image = stitch_images(a, b, H)

cv2.imshow('a', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
