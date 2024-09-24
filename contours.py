import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b1.jpeg', 0)

# 检查图像是否成功加载
if img is None:
    print("Error: Unable to load image. Check the file path and integrity.")
else:
    print(img.shape)

    # 应用二值化阈值
    ret, dst = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY_INV)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个空白图像用于绘制轮廓
    dst2 = np.zeros_like(img)

    # 绘制轮廓
    # cv2.drawContours(dst2, contours, -1, (255, 255, 255), 5)


    for contour in contours:
        cv2.drawContours(dst2, [contour], -1, (255, 255, 255), 1)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        print(f"Contour area: {area}, Perimeter: {perimeter}")

    # 显示原始图像和处理后的图像
    cv2.imshow('img', img)
    cv2.imshow('dst', dst)
    cv2.imshow('dst2', dst2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()