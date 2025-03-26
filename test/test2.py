import cv2
import numpy as np
 
# 读取图片
image = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')
 
# 设置原图中三个点的坐标，用于计算仿射变换矩阵
# 这三个点是原图中的位置，格式为 (x1, y1), (x2, y2), (x3, y3)
# 同时设置变换后这三个点的位置，格式为 (x1', y1'), (x2', y2'), (x3', y3')
pts1 = np.float32([[50,50], [200,50], [50,200]])
pts2 = np.float32([[10,100], [200,50], [100,250]])
 
# 计算仿射变换矩阵
M = cv2.getAffineTransform(pts1, pts2)
 
# 应用仿射变换
dst = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
 
# 显示结果
cv2.imshow('Original', image)
cv2.imshow('Affine Transformed', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
