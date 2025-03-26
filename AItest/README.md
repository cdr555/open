# YOLOv8 目标检测演示

这个项目提供了使用YOLOv8模型进行实时目标检测的演示程序，适用于Mac系统。

## 功能特点

- 实时摄像头目标检测
- 图像文件目标检测
- 视频文件目标检测
- 检测结果保存
- 显示检测FPS（每秒帧数）

## 目录结构

```
├── data/              # 数据目录
│   ├── images/        # 图像数据
│   ├── videos/        # 视频数据
│   └── models/        # 预训练模型
├── src/               # 源代码
│   ├── core/          # 核心功能模块
│   ├── utils/         # 工具函数
│   └── scripts/       # 辅助脚本
├── output/            # 输出结果
└── requirements.txt   # 依赖包列表
```

## 环境要求

- Python 3.8+
- OpenCV
- PyTorch
- Ultralytics（YOLO实现库）

## 安装步骤

1. 克隆或下载此仓库

2. 创建并激活虚拟环境：

```bash
conda create -n yolo-env python=3.x.x

conda activate yolo-env
```

3. 安装依赖包：

```bash
pip install -r requirements.txt
```

4. 首次运行时，程序会自动下载YOLOv8模型（约需10-30MB，取决于所选模型大小）

## 使用方法

项目提供了统一的命令行界面:

```bash
opt/anaconda3/envs/yolo-env/bin/python src/main.py [command] [options]
```

可用的命令:
- `image`: 图像检测
- `video`: 视频检测
- `camera`: 摄像头实时检测

### 实时摄像头检测

```bash
opt/anaconda3/envs/yolo-env/bin/python src/main.py camera
```

- 按 's' 键保存当前检测帧
- 按 'q' 键退出程序

### 图像文件检测

```bash
/opt/anaconda3/envs/yolo-env/bin/python src/main.py image data/images/test.jpg
```

可以设置置信度阈值（默认0.25）：

```bash
/opt/anaconda3/envs/yolo-env/bin/python src/main.py image data/images/test.jpg --conf 0.5
```

### 视频文件检测

```bash
/opt/anaconda3/envs/yolo-env/bin/python src/main.py video path/to/your/video.mp4
```

可用选项：
```bash
# 自定义输出路径
/opt/anaconda3/envs/yolo-env/bin/python src/main.py video path/to/your/video.mp4 --output output/result.mp4

# 调整检测置信度
/opt/anaconda3/envs/yolo-env/bin/python src/main.py video path/to/your/video.mp4 --conf 0.5

# 不保存结果视频，只查看
/opt/anaconda3/envs/yolo-env/bin/python src/main.py video path/to/your/video.mp4 --no-save
```

在视频检测过程中按 'q' 键可随时退出。

## 模型选择

默认使用`yolov8n.pt`（nano版本）模型。如需使用其他版本，修改脚本中的模型路径：

- yolov8n.pt - 最小版本，速度最快
- yolov8s.pt - 小版本，平衡速度和精度
- yolov8m.pt - 中等版本，更高精度
- yolov8l.pt - 大版本，高精度
- yolov8x.pt - 超大版本，最高精度

## 检测结果

- 所有检测结果将保存在`output`目录中
- 文件名包含时间戳，便于区分

## 常见问题

- 如果遇到摄像头无法打开，请检查摄像头连接和权限设置
- 如需使用外接摄像头，修改`cv2.VideoCapture(0)`中的参数（例如`cv2.VideoCapture(1)`）
- Mac系统可能需要在首次运行时授予摄像头访问权限

## 许可证

此项目使用MIT许可证 