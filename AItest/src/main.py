#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.image_detector import detect_objects_in_image
from src.core.video_detector import detect_objects_in_video
from src.core.yolo_demo import main as run_camera_demo

def main():
    parser = argparse.ArgumentParser(description="YOLOv8目标检测工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 图像检测子命令
    image_parser = subparsers.add_parser("image", help="图像目标检测")
    image_parser.add_argument("image_path", help="要检测的图像文件路径")
    image_parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值 (0-1)")
    
    # 视频检测子命令
    video_parser = subparsers.add_parser("video", help="视频目标检测")
    video_parser.add_argument("video_path", help="要处理的视频文件路径")
    video_parser.add_argument("--output", help="输出视频的路径")
    video_parser.add_argument("--conf", type=float, default=0.25, help="置信度阈值 (0-1)")
    video_parser.add_argument("--no-save", action="store_true", help="不保存处理后的视频")
    
    # 摄像头演示子命令
    camera_parser = subparsers.add_parser("camera", help="摄像头实时目标检测")
    
    args = parser.parse_args()
    
    # 如果没有指定子命令，显示帮助
    if not args.command:
        parser.print_help()
        return
    
    # 根据子命令执行相应的功能
    if args.command == "image":
        detect_objects_in_image(args.image_path, args.conf)
    elif args.command == "video":
        detect_objects_in_video(
            args.video_path, 
            args.output, 
            args.conf, 
            not args.no_save
        )
    elif args.command == "camera":
        run_camera_demo()

if __name__ == "__main__":
    main() 