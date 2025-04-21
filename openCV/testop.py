import cv2
import os

flag_file = '/tmp/testop_running.flag'

# 检查并删除旧的标志文件
if os.path.exists(flag_file):
    os.remove(flag_file)

open(flag_file, 'w').close()  # 创建标志文件

try:
    img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

    if img is None:
        print("Error: Unable to open image file.")
    else:
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  # 关闭所有OpenCV窗口
finally:
    os.remove(flag_file)  # 删除标志文件