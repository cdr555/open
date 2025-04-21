import cv2
import numpy as np

class DrawShape:
    def __init__(self):
        self.curshape = 0
        self.startpos = (0, 0)
        self.img = np.zeros((480, 640, 3), np.uint8)
        self.create_window()

    def create_window(self):
        cv2.namedWindow('drawshape', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('drawshape', self.mouse_callback)

    def mouse_callback(self, event, x, y, flags, userdata):
        if (event & cv2.EVENT_LBUTTONDOWN == cv2.EVENT_LBUTTONDOWN):
            self.startpos = (x, y)
        elif (event & cv2.EVENT_LBUTTONUP == cv2.EVENT_LBUTTONUP):
            if self.curshape == 0:
                cv2.line(self.img, self.startpos, (x, y), (0, 0, 255))
            elif self.curshape == 1:
                a = (x - self.startpos[0])
                b = (y - self.startpos[1])
                r = int((a**2 + b**2)**0.5)
                cv2.circle(self.img, self.startpos, r, (0, 255, 0))
            elif self.curshape == 2:
                cv2.ellipse(self.img, (x, y), (100, 50), 0, 0, 360, (255, 0, 0), -1)
            elif self.curshape == 3:
                cv2.rectangle(self.img, self.startpos, (x, y), (0, 0, 255))
            else:
                print('error: no shape')

    def run(self):
        while True:
            cv2.imshow('drawshape', self.img)
            key = cv2.waitKey(0)
            if (key & 0xFF == ord('q')):
                break
            elif (key & 0xFF == ord('l')):
                self.curshape = 0
            elif key == ord('c'):
                self.curshape = 1
            elif key == ord('e'):
                self.curshape = 2
            elif key == ord('r'):
                self.curshape = 3

        cv2.destroyAllWindows()

if __name__ == "__main__":
    draw_shape = DrawShape()
    draw_shape.run()