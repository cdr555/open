import cv2
import numpy as np
#定义一个空的回调函数，当滑动条的值发生变化时会调用这个函数
def callback():
    pass

#创建窗口
cv2.namedWindow('trackbar',cv2.WINDOW_AUTOSIZE)

#创建trackbar（滑动条）
cv2.createTrackbar('R','trackbar',0,255,callback)
cv2.createTrackbar('G','trackbar',0,255,callback)
cv2.createTrackbar('B','trackbar',0,255,callback)

#创建一个背景图片（大小为 480x640 的黑色图像，每个像素有三个通道（RGB），初始值为 0（黑色））
img = np.zeros((480,640,3), np.uint8)

while True:
    #获取当前trackbar（滑动条）值
    r = cv2.getTrackbarPos('R','trackbar')
    g = cv2.getTrackbarPos('G','trackbar')
    b = cv2.getTrackbarPos('B','trackbar')

    #改变背景图片颜色
    img[:] = [b, g, r]
    cv2.imshow('trackbar', img)

    key = cv2.waitKey(10)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()