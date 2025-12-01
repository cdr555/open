import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/b2.png', 0)

# 定义腐蚀操作的核
# kernel = np.zeros((11, 11), np.uint8)
# print(kernel)

# cv2.MORPH_RECT:矩形
# cv2.MORPH_ELLIPSE:椭圆形
# cv2.MORPH_CROSS:十字形
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
#(结构元素形状,核的大小,锚点)
print(kernel)

# # 应用腐蚀操作
# dst = cv2.erode(img, kernel, iterations=1)

# # 应用膨胀操作
# dst2 = cv2.dilate(img,kernel,1)

# 开运算
# dst = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)

# 梯度
# dst = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)

# 顶帽运算
# dst = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)

# 黑帽运算
dst = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)


# 显示原始图像和处理后的图像
cv2.imshow('img', img)
cv2.imshow('dst', dst)
# cv2.imshow('dst2', dst2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 形态学运算（灰度/二值均可）
# 腐蚀 cv2.erode(src,kernel,iterations)：取邻域最小值；白区域变细，小白噪点被去掉。
# 膨胀 cv2.dilate(...)：取邻域最大值；白区域变粗，填小黑洞。
# 开运算 MORPH_OPEN（先腐蚀后膨胀）：去小白噪、平滑边界，不明显改变面积。
# 闭运算 MORPH_CLOSE（先膨胀后腐蚀）：填小黑洞、连通近邻白区。
# 形态学梯度 MORPH_GRADIENT：膨胀减腐蚀，突出边缘。
# 顶帽 MORPH_TOPHAT：原图减开运算，提取“比背景更亮、尺寸小于核”的亮细节。
# 黑帽 MORPH_BLACKHAT：闭运算减原图，提取“比背景更暗、尺寸小于核”的暗细节