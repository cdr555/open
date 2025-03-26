import cv2

# 打开视频文件
cap = cv2.VideoCapture('/Users/itlc00011/Desktop/rr/Test/cars.mov')

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# 加载预训练的 Haar 级联分类器用于车辆检测
car_cascade_path = '/Users/itlc00011/Desktop/rr/Test/haarcascade_car.xml'
car_cascade = cv2.CascadeClassifier(car_cascade_path)

if car_cascade.empty():
    print(f"Error: Unable to load Haar cascade classifier from {car_cascade_path}")
    exit()

# 初始化车辆计数
car_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 检测车辆
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    
    # 绘制检测到的车辆并统计数量
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        car_count += 1
    
    # 显示结果
    cv2.imshow('Vehicle Detection', frame)
    
    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 打印车辆总数
print(f"Total number of vehicles detected: {car_count}")

# 释放资源并关闭窗口
cap.release()
cv2.destroyAllWindows()