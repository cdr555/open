#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import cv2
import numpy as np
from ultralytics import YOLO
import os
import time
from datetime import datetime

def detect_objects_in_video(video_path, output_path=None, confidence=0.25, save_video=True):
    """
    在视频上使用YOLOv8进行目标检测
    """
    # 检查视频是否存在
    if not os.path.exists(video_path):
        print(f"错误：找不到视频 {video_path}")
        return

    # 加载YOLOv8模型
    print("正在加载YOLOv8模型...")
    model = YOLO("data/models/yolov8n.pt")
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误：无法打开视频 {video_path}")
        return
    
    # 获取视频属性
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"视频信息: {width}x{height}, {fps} FPS, 总帧数: {total_frames}")
    
    # 设置输出视频
    if save_video:
        # 如果没有指定输出路径，则自动生成
        if output_path is None:
            # 创建结果目录
            results_dir = "output"
            if not os.path.exists(results_dir):
                os.makedirs(results_dir)
                
            # 生成输出文件名
            base_name = os.path.basename(video_path)
            name, ext = os.path.splitext(base_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(results_dir, f"{name}_detected_{timestamp}.mp4")
        
        # 创建视频编写器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame_count = 0
    start_time = time.time()
    
    # 处理视频帧
    while cap.isOpened():
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # 计算进度百分比
        progress = (frame_count / total_frames) * 100
        if frame_count % 10 == 0:  # 每10帧更新一次进度
            print(f"处理进度: {progress:.1f}% (帧 {frame_count}/{total_frames})")
        
        # 使用YOLO进行目标检测
        results = model(frame, conf=confidence)
        
        # 处理结果
        result = results[0]
        annotated_frame = result.plot()
        
        # 在画面上显示帧编号
        cv2.putText(
            annotated_frame, 
            f"Frame: {frame_count}/{total_frames}", 
            (20, 40), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), 
            2
        )
        
        # 显示检测结果
        cv2.imshow("YOLOv8 视频检测", annotated_frame)
        
        # 保存处理后的帧
        if save_video:
            out.write(annotated_frame)
        
        # 按'q'键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 计算总处理时间
    total_time = time.time() - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    # 释放资源
    cap.release()
    if save_video:
        out.release()
    cv2.destroyAllWindows()
    
    print(f"\n处理完成！")
    print(f"总处理时间: {total_time:.2f} 秒")
    print(f"平均处理速度: {avg_fps:.2f} FPS")
    if save_video:
        print(f"结果已保存到: {output_path}")

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description="YOLOv8视频目标检测")
    parser.add_argument("video_path", help="要处理的视频文件路径")
    parser.add_argument("--output", help="输出视频的路径")
    parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值 (0-1)")
    parser.add_argument("--no-save", action="store_true", help="不保存处理后的视频")
    args = parser.parse_args()
    
    # 执行目标检测
    detect_objects_in_video(
        args.video_path, 
        args.output, 
        args.conf, 
        not args.no_save
    )

if __name__ == "__main__":
    main() 