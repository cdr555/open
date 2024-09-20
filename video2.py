import cv2
#录制视频并保存

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video = cv2.VideoWriter('/Users/itlc00011/Desktop/rr/Test/out3.mp4',fourcc,30,(1280,720))

#创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)

#获取视频设备(摄像头）/从视频文件中读取视频帧
cap = cv2.VideoCapture(0)

#判断摄像头是否为打开状态
while cap.isOpened():

    #从摄像头读视频帧数
    ret, frame = cap.read()
    if ret == True:

      #将视频帧在窗口显示
      cv2.imshow('video', frame)

      #重新将窗口设定为指定大小
      cv2.resizeWindow('video',640,480)

      #写数据到多媒体文件
      video.write(frame)

      #q退出,帧与真之间停留时间
      key = cv2.waitKey(5)
      if key & 0xFF == ord('q'):
          break
    else:
        break
#释放VideoCapture
cap.release()

#释放VideoWrite
video.release()

cv2.destroyAllWindows()