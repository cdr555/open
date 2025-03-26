#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cv2
import numpy as np
from ultralytics import YOLO
import os
from datetime import datetime

def detect_objects_in_image(image_path, confidence=0.25):
    """
    在单个图像上使用YOLOv8进行目标检测
    """
    # 检查图像是否存在
    if not os.path.exists(image_path):
        print(f"错误：找不到图像 {image_path}")
        return

    # 加载YOLOv8模型
    print("正在加载YOLOv8模型...")
    model = YOLO("data/models/yolov8n.pt")  # 使用YOLOv8 nano模型
    
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误：无法读取图像 {image_path}")
        return
        
    # 使用YOLO进行目标检测
    print("正在进行目标检测...")
    results = model(image, conf=confidence)
    
    # 处理并显示结果
    result = results[0]
    annotated_image = result.plot()
    
    # 检测到的目标信息
    boxes = result.boxes
    detected_classes = []
    
    # 打印检测结果
    print("\n检测到的对象:")
    for box in boxes:
        class_id = int(box.cls[0].item())
        class_name = result.names[class_id]
        confidence = box.conf[0].item()
        detected_classes.append(class_name)
        print(f"- {class_name}: 置信度 {confidence:.2f}")
    
    # 创建结果目录
    results_dir = "output"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    # 保存结果图像
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(results_dir, f"{name}_detected_{timestamp}{ext}")
    cv2.imwrite(output_path, annotated_image)
    
    print(f"\n检测到 {len(boxes)} 个对象")
    print(f"结果已保存到 {output_path}")
    
    # 显示结果图像
    cv2.imshow("检测结果", annotated_image)
    print("按任意键关闭窗口")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="YOLOv8图像目标检测")
    parser.add_argument("image_path", help="要检测的图像文件路径")
    parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值 (0-1)")
    args = parser.parse_args()
    
    # 执行目标检测
    detect_objects_in_image(args.image_path, args.conf)

if __name__ == "__main__":
    main() 