import cv2
import numpy as np

# 读取图像并转换为灰度图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b5.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Shi-Tomasi 角点检测(灰度图像, 最大角点数, 角点质量取值范围0～1, 最小欧式距离)
corners = cv2.goodFeaturesToTrack(gray, maxCorners=10, qualityLevel=0.9, minDistance=30)
# 将角点坐标转换为整数类型
corners = np.int64(corners)

# 在图像上标记角点
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

# 显示结果
cv2.imshow('Shi-Tomasi Corners', img)
cv2.waitKey(0)
cv2.destroyAllWindows()