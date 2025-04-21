import cv2
import numpy as np

curshape = 0
startpos = (0, 0)

def mouse_callback(event, x, y, flags, userdata):
    global startpos  # 声明 startpos 为全局变量
    if (event & cv2.EVENT_LBUTTONDOWN == cv2.EVENT_LBUTTONDOWN):
        startpos = (x, y)
    elif (event & cv2.EVENT_LBUTTONUP == cv2.EVENT_LBUTTONUP):
        if curshape == 0:
            cv2.line(img, startpos, (x, y), (0, 0, 255))
        elif curshape == 1:
            a = (x - startpos[0])
            b = (y - startpos[1])
            r = int((a**2+b**2)**0.5)
            cv2.circle(img, startpos, r, (0, 255, 0))
        elif curshape == 2:
            cv2.ellipse(img, (x, y), (100, 50), 0, 0, 360, (255, 0, 0), -1)
        elif curshape == 3:
            cv2.rectangle(img,startpos,(x,y),(0,0,255))
        else:
            print('error: no shape')

cv2.namedWindow('drawshape', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('drawshape', mouse_callback)

img = np.zeros((480, 640, 3), np.uint8)

while True:
    cv2.imshow('drawshape', img)
    key = cv2.waitKey(0)
    if (key & 0xFF == ord('q')):
        break
    elif (key & 0xFF == ord('l')):
        curshape = 0
    elif key == ord('c'):
        curshape = 1
    elif key == ord('e'):
        curshape = 2
    elif key == ord('r'):
        curshape = 3

cv2.destroyAllWindows()