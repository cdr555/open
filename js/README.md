# 位图转矢量图工具

这是一个基于 Potrace 库的位图(PNG, JPEG等)到矢量图(SVG)的转换工具。

## 功能特点

- 将单个位图转换为SVG
- 支持彩色图像的处理
- 批量转换整个目录的图片
- 提供命令行工具，方便从终端使用
- 可自定义转换参数

## 安装

### 安装依赖

```bash
npm install
```

```bash
# 运行单个图片转换示例
npm run simple

# 运行彩色图片转换示例
npm run color

# 运行批量转换示例
npm run batch
```

## 参数说明

- `threshold`: 阈值，用于将图像转换为黑白 (0-255，默认128)
- `turdSize`: 忽略小于此尺寸的区域，可用于去除噪点 (默认2)
- `optCurve`: 是否优化曲线 (默认true)
- `alphaMax`: 最大角度 (默认1)
- `optTolerance`: 优化容差 (默认0.2)
- `color`: 输出SVG的颜色 (默认#000000)

## 注意事项

1. 对于复杂图像，转换过程可能需要一些时间
2. 转换质量取决于原始图像的质量和清晰度
3. 参数调整对最终效果有很大影响，可能需要多次尝试
4. 彩色图像会被转换为单色SVG，如果需要彩色效果，可能需要额外处理

## 依赖库

- [potrace](https://www.npmjs.com/package/potrace): 位图追踪库
- [jimp](https://www.npmjs.com/package/jimp): 图像处理库
- [fs-extra](https://www.npmjs.com/package/fs-extra): 增强的文件系统操作 