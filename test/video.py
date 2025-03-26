import cv2
#播放

#创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)

#获取视频设备(摄像头）/从视频文件中读取视频帧
cap = cv2.VideoCapture('/Users/itlc00011/Desktop/rr/Test/aaa.MOV')

#判断摄像头是否为打开状态
while cap.isOpened:

    #从摄像头读视频帧数
    ret, frame = cap.read(5)
    if not ret:
        print("Failed to grab frame")
        break
    #将视频帧在窗口显示
    cv2.imshow('video', frame)

    #q退出,帧与真之间停留时间
    key = cv2.waitKey(5)
    if key & 0xFF == ord('q'):
        break
#释放VideoCapture
cap.release()
cv2.destroyAllWindows()