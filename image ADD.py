import cv2
import numpy as np

#1920*1080
a = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

# print(a.shape)

#确保 b 的形状与 a 相同
b = np.ones(a.shape,np.uint8) * 200
b = cv2.imread('/Users/itlc00011/Desktop/rr/Test/111.png')

cv2.imshow('a',a)
result = cv2.add(a,b)
cv2.imshow('image ADD',result)
cv2.waitKey(0)
cv2.destroyAllWindows()