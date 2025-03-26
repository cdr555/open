import cv2

# 读取图像文件,0表示灰色
image = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg',0)

# 检查图像是否成功加载
if image is None:
    print("Error: Could not load image.")
    exit()

# 创建一个可调整大小的窗口
cv2.namedWindow('new', cv2.WINDOW_NORMAL)
# q退出，s保存，其他键保留原窗口
while True:
# 显示图像
  cv2.imshow('new', image)

# 等待按键
  key = cv2.waitKey(0)
  if (key & 0xFF == ord('q')):
    break
  elif(key & 0xFF == ord('s')):

    #将 image 图像保存到 /Users/itlc00011/Desktop/rr/Test/111.png 路径下，文件格式为 PNG
    cv2.imwrite('/Users/itlc00011/Desktop/rr/Test/111.png',image)
  else:
     print(key)
cv2.destroyAllWindows()