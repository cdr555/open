import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')
new = cv2.resize(img,(540,960),cv2.INTER_AREA)
#将 cv2.INTER_AREA 参数指定为关键字参数 interpolation
new1 = cv2.resize(img,None,fx=0.3,fy=0.3,interpolation=cv2.INTER_AREA)

print(img.shape)

cv2.imshow('img',img)
cv2.imshow('new',new)
cv2.imshow('new1',new1)
cv2.waitKey(0)