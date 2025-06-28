import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def detect_faces(self, image_path):
        """检测人脸并过滤误检测"""
        img = cv2.imread(r'D:\open\openCV\test_faces\single_face.jpg')
        if img is None:
            print(f"错误：无法读取图片 {image_path}")
            return
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)  # 改善图像对比度
        
        # 人脸检测
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.05,
            minNeighbors=20,
            minSize=(80, 80),
            maxSize=(400, 400)
        )
        
        print(f"初步检测到 {len(faces)} 张人脸")
        
        # 智能过滤误检测
        if len(faces) > 1:
            faces = self.filter_false_detections(faces)
        
        print(f"最终检测到 {len(faces)} 张人脸")
        
        # 绘制结果
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, f'Face {i+1}', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        cv2.imshow('人脸检测', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def filter_false_detections(self, faces):
        """过滤掉明显的误检测"""
        areas = [w * h for x, y, w, h in faces]
        max_area = max(areas)
        
        filtered = []
        for face, area in zip(faces, areas):
            x, y, w, h = face
            area_ratio = area / max_area
            
            # 保留面积至少是最大面积25%且最小边长80像素的检测框
            if area_ratio >= 0.25 and min(w, h) >= 80:
                filtered.append(face)
        
        return np.array(filtered) if filtered else faces

# 使用示例
if __name__ == "__main__":
    detector = FaceDetector()
    detector.detect_faces(r'D:\open\openCV\test_faces\single_face.jpg')
