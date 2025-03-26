import cv2
import numpy as np

# 定义参数
min_w = 90
min_h = 90
line_high = 150
offset = 8
carno = 0
cars = []

# 计算中心点的函数
def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# 打开视频文件
cap = cv2.VideoCapture('/Users/itlc00011/Desktop/rr/Test/cars.mov')

# 创建背景减法器和形态学核
bgsubmog = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 应用高斯模糊
    blur = cv2.GaussianBlur(gray, (3, 3), 5)
    
    # 应用背景减法器
    mask = bgsubmog.apply(blur)
    
    # 形态学操作
    erode = cv2.erode(mask, kernel)
    dilate = cv2.dilate(erode, kernel, iterations=3)
    close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    
    # 查找轮廓
    cnts, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # 绘制检测线
    cv2.line(frame, (5, line_high), (1250, line_high), (255, 0, 255), 3)
    
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        
        # 验证检测到的轮廓是否为有效车辆
        isValid = (w >= min_w) and (h >= min_h)
        if not isValid:
            continue
        
        # 绘制矩形框和中心点
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cpoint = center(x, y, w, h)
        cars.append(cpoint)
        cv2.circle(frame, cpoint, 5, (0, 0, 255), -1)
        
        # 计数车辆
        for (cx, cy) in cars:
            if (cy > line_high - offset) and (cy < line_high + offset):
                carno += 1
                cars.remove((cx, cy))
                print(carno)
    
    # 显示车辆计数
    cv2.putText(frame, "Cars Count:" + str(carno), (500, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    
    # 显示结果
    cv2.imshow('video', frame)
    
    # 按 'ESC' 键退出
    key = cv2.waitKey(1)
    if key == 27:
        break

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()
