# complete_test.py
import sys
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

print("\n=== 包测试 ===")

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
    
    # 简单的PyTorch测试
    x = torch.randn(2, 3)
    print(f"   PyTorch张量: {x.shape}")
except ImportError as e:
    print(f"❌ PyTorch: {e}")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow: {tf.__version__}")
    
    # 简单的TensorFlow测试
    y = tf.constant([[1, 2], [3, 4]])
    print(f"   TensorFlow张量: {y.shape}")
except ImportError as e:
    print(f"❌ TensorFlow: {e}")

try:
    import numpy as np
    import pandas as pd
    import sklearn
    import matplotlib.pyplot as plt
    
    print(f"✅ NumPy: {np.__version__}")
    print(f"✅ Pandas: {pd.__version__}")
    print(f"✅ Scikit-learn: {sklearn.__version__}")
    
    # k-NN快速测试
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.datasets import make_classification
    
    X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    accuracy = knn.score(X, y)
    print(f"✅ k-NN测试准确率: {accuracy:.3f}")
    
except ImportError as e:
    print(f"❌ 其他库: {e}")

print("\n🎉 所有环境配置完成！可以开始机器学习项目了！")