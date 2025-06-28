import os
import urllib.request
import cv2
import numpy as np

def download_test_faces():
    """下载一些用于测试的人脸图片"""
    
    # 创建测试图片目录
    test_dir = "test_faces"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 一些免费的测试图片URL（来自Unsplash等网站）
    test_urls = {
        "single_face.jpg": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
        "group_faces.jpg": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400",
        "child_face.jpg": "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d?w=400",
        "elderly_face.jpg": "https://images.unsplash.com/photo-1566616213894-2d4e1baee5d8?w=400",
    }
    
    print("开始下载测试图片...")
    
    for filename, url in test_urls.items():
        filepath = os.path.join(test_dir, filename)
        try:
            print(f"正在下载: {filename}")
            urllib.request.urlretrieve(url, filepath)
            print(f"✓ 已下载: {filename}")
        except Exception as e:
            print(f"✗ 下载失败 {filename}: {e}")
    
    print(f"\n图片已下载到 {test_dir} 目录")
    
def create_synthetic_faces():
    """创建一些合成的测试图片"""
    
    test_dir = "test_faces"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    print("\n创建合成测试图片...")
    
    # 创建一个包含多个圆形（模拟人脸）的测试图片
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # 绘制一些圆形作为"人脸"
    faces_positions = [
        (200, 200, 80),  # (x, y, radius)
        (400, 200, 70),
        (600, 200, 90),
        (300, 400, 75),
        (500, 400, 85)
    ]
    
    for x, y, r in faces_positions:
        # 绘制脸部轮廓
        cv2.circle(img, (x, y), r, (200, 180, 160), -1)
        cv2.circle(img, (x, y), r, (100, 100, 100), 2)
        
        # 绘制眼睛
        eye_offset = r // 3
        cv2.circle(img, (x - eye_offset, y - eye_offset), r // 8, (50, 50, 50), -1)
        cv2.circle(img, (x + eye_offset, y - eye_offset), r // 8, (50, 50, 50), -1)
        
        # 绘制嘴巴
        cv2.ellipse(img, (x, y + r // 3), (r // 2, r // 4), 0, 0, 180, (100, 50, 50), 2)
    
    # 保存合成图片
    cv2.imwrite(os.path.join(test_dir, "synthetic_faces.jpg"), img)
    print("✓ 已创建: synthetic_faces.jpg")
    
    # 创建一个空白图片（用于测试无人脸的情况）
    blank = np.ones((400, 600, 3), dtype=np.uint8) * 240
    cv2.putText(blank, "No Face Image", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)
    cv2.imwrite(os.path.join(test_dir, "no_face.jpg"), blank)
    print("✓ 已创建: no_face.jpg")

def test_detection_on_downloaded():
    """在下载的图片上测试人脸检测"""
    
    test_dir = "test_faces"
    if not os.path.exists(test_dir):
        print("测试目录不存在，请先运行下载功能")
        return
    
    # 加载人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("\n测试人脸检测...")
    
    # 测试目录中的所有图片
    for filename in os.listdir(test_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(test_dir, filename)
            img = cv2.imread(filepath)
            
            if img is None:
                continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            
            print(f"{filename}: 检测到 {len(faces)} 张人脸")
            
            # 绘制检测结果
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # 保存检测结果
            result_path = os.path.join(test_dir, f"detected_{filename}")
            cv2.imwrite(result_path, img)

def main():
    """主函数"""
    print("人脸测试图片工具")
    print("=" * 50)
    print("1. 下载测试图片（从网络）")
    print("2. 创建合成测试图片")
    print("3. 在下载的图片上测试检测")
    print("4. 全部执行")
    print("5. 退出")
    
    choice = input("\n请选择功能 (1-5): ")
    
    if choice == '1':
        download_test_faces()
    elif choice == '2':
        create_synthetic_faces()
    elif choice == '3':
        test_detection_on_downloaded()
    elif choice == '4':
        download_test_faces()
        create_synthetic_faces()
        test_detection_on_downloaded()
    elif choice == '5':
        print("退出程序")
    else:
        print("无效选择")

if __name__ == "__main__":
    main() 