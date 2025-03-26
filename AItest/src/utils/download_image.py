#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os

def download_image(url, filename):
    print(f"正在从 {url} 下载图片...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = os.path.getsize(filename) / 1024  # KB
        print(f"下载成功！保存为 {filename} (大小: {file_size:.2f} KB)")
        return True
    else:
        print(f"下载失败，状态码: {response.status_code}")
        return False

if __name__ == "__main__":
    # 尝试几个不同的图片源
    urls = [
        "https://raw.githubusercontent.com/ultralytics/assets/main/im/zidane.jpg",
        "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg",
        "https://raw.githubusercontent.com/ultralytics/assets/master/im/bus.jpg"
    ]
    
    for i, url in enumerate(urls):
        filename = f"test_image_{i+1}.jpg"
        if download_image(url, filename):
            print(f"成功下载图片 {i+1}")
            break
    else:
        print("所有图片源下载失败") 