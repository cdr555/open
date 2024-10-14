import cv2
import numpy as np

img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1184.jpg')
img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/IMG_1185.jpg')
img1 = cv2.resize(img1, (4000, 6048))
img2 = cv2.resize(img2, (4000, 6048))

def stitch_images(img1, img2, H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)

    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

    translation_dist = [-x_min, -y_min]

    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max - x_min, y_max - y_min))
    output_img[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = img1

    return output_img

def get_homo(img1, img2):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
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

imputs = np.hstack((img1, img2))

H = get_homo(img1, img2)

result_image = stitch_images(img1, img2, H)

cv2.imshow('a', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
