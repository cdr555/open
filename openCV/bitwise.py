import cv2
import numpy as np
#创建两个空白图像(黑色图像)
img1 = np.zeros((200,200),np.uint8)
img2 = np.zeros((200,200),np.uint8)

#将img1的(20:120,20:120)区域设置为白色
img1[20:120,20:120] = 255
#将img2的(80:180,80:180)区域设置为白色
img2[80:180,80:180] = 255

img3 = cv2.bitwise_not(img1)
# img4 = cv2.bitwise_and(img1,img2)
# img5 = cv2.bitwise_or(img1,img2)
# img6 = cv2.bitwise_xor(img1,img2)


cv2.imshow('img1',img1)
cv2.imshow('img2',img2)
cv2.imshow('img3',img3)
# cv2.imshow('img4',img4)
# cv2.imshow('img5',img5)
# cv2.imshow('img6',img6)
cv2.waitKey(0)
