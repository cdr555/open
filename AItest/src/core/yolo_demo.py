#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from ultralytics import YOLO
import os
import time
from datetime import datetime

def main():
    print("正在初始化YOLOv8模型...")
    
    # 加载YOLOv8模型
    model = YOLO("data/models/yolov8n.pt")  # 使用n(nano)版本，您也可以选择s(small)、m(medium)、l(large)、x(xlarge)
    
    # 检查是否有摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头，请检查连接")
        return
    
    # 创建保存检测结果的目录
    results_dir = "output"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    print("YOLOv8模型已加载，按'q'键退出演示")
    
    while True:
        # 读取摄像头帧
        ret, frame = cap.read()
        if not ret:
            print("无法从摄像头获取画面")
            break
            
        # 使用YOLO进行目标检测
        start_time = time.time()
        results = model(frame)
        inference_time = time.time() - start_time
        
        # 处理结果
        result = results[0]
        annotated_frame = result.plot()
        
        # 在画面上显示FPS
        fps = 1.0 / inference_time
        cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 显示检测结果
        cv2.imshow("YOLOv8 目标检测", annotated_frame)
        
        # 按's'键保存当前帧
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(results_dir, f"detection_{timestamp}.jpg")
            cv2.imwrite(save_path, annotated_frame)
            print(f"已保存检测结果到 {save_path}")
        
        # 按'q'键退出
        if key == ord('q'):
            break
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("演示已结束")

if __name__ == "__main__":
    main() 