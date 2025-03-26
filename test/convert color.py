import cv2
#import numpy as np

def callback(x):
    pass

# 创建窗口
cv2.namedWindow('color', cv2.WINDOW_AUTOSIZE)

# 读取图片
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

# 定义颜色空间转换代码
colorspace = [cv2.COLOR_BGR2BGRA, cv2.COLOR_BGR2RGBA, cv2.COLOR_BGR2GRAY,
              cv2.COLOR_BGR2HSV_FULL, cv2.COLOR_BGR2YUV]

# 创建滑动条
cv2.createTrackbar('colorbar', 'color', 0, len(colorspace) - 1, callback)

# 创建一个背景图片
# img = np.zeros((480, 640, 3), np.uint8)

while True:
    # 获取当前滑动条的值
    index = cv2.getTrackbarPos('colorbar', 'color')

    # 颜色空间转换API
    cvt_img = cv2.cvtColor(img, colorspace[index])

    # 显示转换后的图像
    cv2.imshow('color', cvt_img)

    key = cv2.waitKey(10)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()