import cv2
import numpy as np
#读取图像
img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/small2.png')
img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/big2.png')
#灰度图
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#创建特征检测器
sift = cv2.xfeatures2d.SIFT_create()
#计算特征点与描述子
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)
#创建匹配器
index_params = dict(algorithm=1, trees=5)
search_params = dict(check = 50)
flann = cv2.FlannBasedMatcher(index_params,search_params)
#进行特征匹配
matches = flann.knnMatch(des1, des2, k=2)
#遍历每个匹配对m，n，筛选符合的进入good[]
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])

# 绘制匹配点       
# img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
if len(good) > 4:
    srcPts = np.float32([kp1[m[0].queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dstPts = np.float32([kp2[m[0].trainIdx].pt for m in good]).reshape(-1, 1, 2)
    #计算单应性矩阵
    H, _ = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)
    
    h, w = img1.shape[:2]
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, H)
    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good), 4))
    matchesMask = None
    exit()


img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
cv2.imshow('matches', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
