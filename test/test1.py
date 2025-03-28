import cv2
#####
cv2.namedWindow('test1',cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret:
        print('f')
        break
    cv2.imshow('test1',frame)
    key = cv2.waitKey(5)
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()