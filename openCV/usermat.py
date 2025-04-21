import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

#shape属性中包括三个信息，高度，长度，通道数
print(img.shape)

#size 图像占用多大空间
#高度 * 长度 * 通道数
print(img.size)

#图像中每个元素的位深
print(img.dtype)