import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg',0)

#第一个返回值是阈值（这里用 _ 忽略）
#第二个返回值是处理后的图像
_,dst = cv2.threshold(img,100,50,cv2.THRESH_BINARY_INV)

cv2.imshow('img',img)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()