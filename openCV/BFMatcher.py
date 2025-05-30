import cv2
import numpy as np
img1 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/small2.png')
img2 = cv2.imread('/Users/itlc00011/Desktop/rr/Test/big2.png')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(gray1, None)
kp2, des2 = orb.detectAndCompute(gray2, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
# matches = sorted(matches, key=lambda x: x.distance)
# img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches,None)
cv2.imshow('matches', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()