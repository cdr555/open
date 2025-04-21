import cv2
#创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
#获取视频设备（摄像头）
cap = cv2.VideoCapture(0)

while True:
    #从摄像头读视频帧数
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
#将视频帧在窗口显示
    cv2.imshow('video', frame)
#q退出
    key = cv2.waitKey(5)
    if key & 0xFF == ord('q'):
        break
#释放VideoCapture
cap.release()
cv2.destroyAllWindows()