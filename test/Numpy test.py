import numpy as np
import cv2
# a = np.array([2,3,4])
# b = np.array([[1,2,3],[4,5,6]])
# print(a)
# print(b)

# zeros全0
# c = np.zeros((4,4,3),np.uint8)
# print(c)

# #ones全1
# d = np.ones((4,4,3),np.uint8)
# print(d)

# #255表示数值，可自定义
# e = np.full((4,4,3),255,np.uint8)
# print(e)

#斜对角是1，其它为0
# f = np.identity(3)
# print(f)

#第一行第二个开始，斜对角为1
# g = np.eye(5,7, k=1)
# print(g)



# # 创建一个空白图像
# img = np.zeros((300, 300,3), np.uint8)

# # 打印图像中 (100, 100) 位置的像素值
# print(img[100, 100])

# # 将图像中 (0, 100) 到 (199, 100) 的像素值设置为 255（白色）
# count = 0
# while count < 200:
#     #BGR的顺序012
#     img[count, 100,1] = 255  #还可以 = [0, 0, 255] B,G通道为0，R通道为255
#     count = count + 1

# # 显示图像
# cv2.imshow('img', img)
# key = cv2.waitKey(0)
# if key & 0xFF == ord('q'):
#     cv2.destroyAllWindows()

img = np.zeros((300, 300,3), np.uint8)

#定义一个感兴趣区域（ROI），从图像的 (100, 100) 到 (200, 200)
roi = img[100:200,100:200]

#将第一个 ROI 的所有像素值设置为 [0, 0, 255]（红色），roi[:,:] = roi[:]
roi[:,:] = [0,0,255]

#在第一个 ROI 内部定义一个从 (10, 10) 到 (90, 90) 的第二个 ROI，并将其所有像素值设置为 [0, 255, 0]（绿色）
roi[10:90,10:90] = [0,255,0]

roi[20:60,20:60] = [255,0,0]
cv2.imshow('img', roi)
key = cv2.waitKey(0)
if key & 0xFF == ord('q'):
    cv2.destroyAllWindows()