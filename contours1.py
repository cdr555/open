import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b1.jpeg', 0)

# 应用二值化阈值
ret, dst = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

# 查找轮廓
contours, _ = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 创建空白图像用于绘制轮廓、多边形逼近、凸包和外接矩形
dst2 = np.zeros_like(img)
dst3 = np.zeros_like(img)
dst4 = np.zeros_like(img)
dst5 = np.zeros_like(img)
dst6 = np.zeros_like(img)

# 绘制轮廓、多边形逼近、凸包和外接矩形
for contour in contours:
    # 绘制原始轮廓
    cv2.drawContours(dst2, [contour], -1, (255, 255, 255), 1)
    
    # 多边形逼近
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    cv2.drawContours(dst3, [approx], -1, (255, 255, 255), 1)
    
    # 凸包
    hull = cv2.convexHull(contour)
    cv2.drawContours(dst4, [hull], -1, (255, 255, 255), 1)
    
    # 外接最大矩形
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(dst5, (x, y), (x + w, y + h), (255, 255, 255), 1)
    
    # 最小外接矩形
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(dst6, [box], 0, (255, 255, 255), 1)
    
    # 计算面积和周长
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    print(f"Contour area: {area}, Perimeter: {perimeter}")

# 显示图像
cv2.imshow('Original Contours', dst2)
cv2.imshow('Polygon Approximation', dst3)
cv2.imshow('Convex Hull', dst4)
cv2.imshow('Bounding Rectangles', dst5)
cv2.imshow('Min Area Rectangles', dst6)
cv2.waitKey(0)
cv2.destroyAllWindows()