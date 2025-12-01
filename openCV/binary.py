import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg',0)

#第一个返回值是阈值（这里用 _ 忽略）
#第二个返回值是处理后的图像
_,dst = cv2.threshold(img,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow('img',img)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 函数签名
# ret, dst = cv2.threshold(src, thresh, maxval, type)
# 参数
# src：输入图像。单通道灰度，支持 uint8 或 float32。彩色需先转灰度。
# thresh：阈值（手动模式下生效）。若使用自动阈值（OTSU/ TRIANGLE），请传 0。
# maxval：二值化时的高值（仅对 THRESH_BINARY/THRESH_BINARY_INV 有效，其他类型会忽略）。
# type：阈值类型（可与 OTSU/ TRIANGLE 通过“加号”组合）：
# THRESH_BINARY：dst = maxval if src > thresh else 0
# THRESH_BINARY_INV：dst = 0 if src > thresh else maxval
# THRESH_TRUNC：dst = thresh if src > thresh else src（忽略 maxval）
# THRESH_TOZERO：dst = src if src > thresh else 0（忽略 maxval）
# THRESH_TOZERO_INV：dst = 0 if src > thresh else src（忽略 maxval）
# + THRESH_OTSU：大津法自动选阈值（8-bit 单通道），常与 BINARY/INV 组合，thresh 置 0
# + THRESH_TRIANGLE：三角法自动选阈值（单峰直方图更稳），同样与 BINARY/INV 组合，thresh 置 0
# 返回值
# ret：实际使用的阈值（手动模式=输入的 thresh；OTSU/ TRIANGLE 模式=自动计算结果）。
# dst：阈值化后的输出图。
# 灰度图（Grayscale）
# 单通道图像，每像素表示亮度。
# 常见取值范围：uint8 的 0–255（0=黑，255=白）。
# 二值图（Binary/Mask）
# 单通道但只有两类取值，常用 0 和 255（也可用 0 和 1 作为逻辑掩码）。