import cv2
import numpy as np
# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b5.jpeg')
gary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 创建 SIFT 检测器
sift = cv2.xfeatures2d.SIFT_create()
kp,des = sift.detectAndCompute(gary, None)
print(des[0])
img = cv2.drawKeypoints(gary, kp, img)
cv2.imshow('sift_keypoints', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

