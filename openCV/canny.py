import cv2
import numpy as np

img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg',0)

blur = cv2.GaussianBlur(img,(3,3),1.0)
v = np.median(blur)
lower = int(max(0, (1.0 - 0.33) * v)) #低阈值
upper = int(min(255, (1.0 + 0.33) * v)) #高阈值
#Canny三个参数(输入图像,低阈值,高阈值)
dst = cv2.Canny(blur,lower,upper,L2gradient=True)

cv2.imshow('img',img)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()