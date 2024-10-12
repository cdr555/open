import cv2
import numpy as np
img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/small2.png')
img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/big2.png')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)
index_params = dict(algorithm=1, trees=5)
search_params = dict(check = 50)
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1, des2, k=2)
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
cv2.imshow('matches', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
