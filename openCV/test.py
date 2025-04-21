import cv2

cv2.namedWindow('test',cv2.WINDOW_AUTOSIZE)
img = cv2.imread('/Users/itlc00011/Desktop/rr/Test/aa.jpeg')

while True:
    cv2.imshow('test',img)
    key = cv2.waitKey()
    if key &0xFF == ord('q'):
        break

cv2.destroyAllWindows()