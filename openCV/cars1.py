import cv2
import numpy as np

# 加载 YOLO 模型
net = cv2.dnn.readNet('/Users/itlc00011/Desktop/rr/Test/yolov3.weights', '/Users/itlc00011/Desktop/rr/Test/yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# 加载 COCO 类别名称
with open('/Users/itlc00011/Desktop/rr/Test/coco.names.txt', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# 打开视频文件
cap = cv2.VideoCapture('/Users/itlc00011/Desktop/rr/Test/cars.mov')

if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# 初始化车辆计数
car_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    height, width, channels = frame.shape

    # 创建 YOLO 输入
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # 解析 YOLO 输出
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'car':
                # 车辆检测
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 非极大值抑制
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    current_car_count = 0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            current_car_count += 1

    # 更新总车辆计数
    car_count += current_car_count

    # 在窗口中显示当前检测到的车辆数量
    cv2.putText(frame, f"Current Cars: {current_car_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Total Cars: {car_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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