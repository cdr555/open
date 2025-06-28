"""
k-最近邻算法 (k-Nearest Neighbors, k-NN) 详细实现
作者: AI Assistant
日期: 2024

k-NN是一种简单而有效的监督学习算法，用于分类和回归任务。
算法原理：对于新的数据点，找到训练集中距离最近的k个邻居，
然后基于这些邻居的标签进行预测。
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class KNearestNeighbors:
    """
    k-最近邻算法实现类
    
    参数:
    - k: 邻居数量，默认为3
    - distance_metric: 距离度量方法，支持'euclidean', 'manhattan', 'minkowski'
    - p: Minkowski距离的参数，当p=1时为曼哈顿距离，p=2时为欧几里得距离
    """
    
    def __init__(self, k=3, distance_metric='euclidean', p=2):
        self.k = k
        self.distance_metric = distance_metric
        self.p = p
        self.X_train = None
        self.y_train = None
        
    def fit(self, X, y):
        """
        训练模型（实际上是存储训练数据）
        
        参数:
        - X: 训练特征数据，形状为 (n_samples, n_features)
        - y: 训练标签数据，形状为 (n_samples,)
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)
        
    def _calculate_distance(self, x1, x2):
        """
        计算两个数据点之间的距离
        
        参数:
        - x1, x2: 两个数据点
        
        返回:
        - 距离值
        """
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        elif self.distance_metric == 'minkowski':
            return np.power(np.sum(np.abs(x1 - x2) ** self.p), 1/self.p)
        else:
            raise ValueError(f"不支持的距离度量方法: {self.distance_metric}")
    
    def _get_neighbors(self, x):
        """
        获取距离查询点最近的k个邻居
        
        参数:
        - x: 查询点
        
        返回:
        - k个最近邻居的索引
        """
        distances = []
        for i, x_train in enumerate(self.X_train):
            dist = self._calculate_distance(x, x_train)
            distances.append((dist, i))
        
        # 按距离排序并返回前k个邻居的索引
        distances.sort(key=lambda x: x[0])
        neighbors = [distances[i][1] for i in range(self.k)]
        return neighbors
    
    def predict(self, X):
        """
        对新数据进行预测
        
        参数:
        - X: 测试数据，形状为 (n_samples, n_features)
        
        返回:
        - 预测结果数组
        """
        if self.X_train is None or self.y_train is None:
            raise ValueError("模型尚未训练，请先调用fit方法")
        
        X = np.array(X)
        predictions = []
        
        for x in X:
            neighbors = self._get_neighbors(x)
            neighbor_labels = [self.y_train[i] for i in neighbors]
            
            # 对于分类任务，使用投票机制
            if self._is_classification():
                prediction = Counter(neighbor_labels).most_common(1)[0][0]
            # 对于回归任务，使用平均值
            else:
                prediction = np.mean(neighbor_labels)
            
            predictions.append(prediction)
        
        return np.array(predictions)
    
    def _is_classification(self):
        """
        判断是分类任务还是回归任务
        """
        # 如果标签是整数且种类较少，认为是分类任务
        unique_labels = np.unique(self.y_train)
        return len(unique_labels) <= 20 and all(isinstance(label, (int, np.integer)) for label in unique_labels)
    
    def predict_proba(self, X):
        """
        预测类别概率（仅适用于分类任务）
        
        参数:
        - X: 测试数据
        
        返回:
        - 每个类别的概率
        """
        if not self._is_classification():
            raise ValueError("predict_proba仅适用于分类任务")
        
        X = np.array(X)
        probabilities = []
        classes = np.unique(self.y_train)
        
        for x in X:
            neighbors = self._get_neighbors(x)
            neighbor_labels = [self.y_train[i] for i in neighbors]
            
            # 计算每个类别的概率
            label_counts = Counter(neighbor_labels)
            probs = []
            for cls in classes:
                probs.append(label_counts.get(cls, 0) / self.k)
            
            probabilities.append(probs)
        
        return np.array(probabilities)

def calculate_accuracy(y_true, y_pred):
    """计算分类准确率"""
    return np.mean(y_true == y_pred)

def calculate_mse(y_true, y_pred):
    """计算均方误差"""
    return np.mean((y_true - y_pred) ** 2)

def plot_classification_results(X, y, X_test, y_test, y_pred, title="k-NN分类结果"):
    """可视化分类结果"""
    plt.figure(figsize=(15, 6))
    plt.suptitle(title, fontsize=16, fontweight='bold')
    
    # 训练数据
    plt.subplot(1, 2, 1)
    scatter1 = plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', alpha=0.7, s=50)
    plt.title('训练数据分布', fontsize=14, pad=20)
    plt.xlabel('特征1', fontsize=12)
    plt.ylabel('特征2', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.colorbar(scatter1, label='类别')
    
    # 设置坐标轴刻度
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # 测试结果
    plt.subplot(1, 2, 2)
    scatter2 = plt.scatter(X_test[:, 0], X_test[:, 1], c=y_pred, cmap='viridis', alpha=0.7, s=50)
    plt.title('测试预测结果', fontsize=14, pad=20)
    plt.xlabel('特征1', fontsize=12)
    plt.ylabel('特征2', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.colorbar(scatter2, label='预测类别')
    
    # 设置坐标轴刻度
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    plt.tight_layout()
    plt.show()

def plot_k_performance(k_values, accuracies, mse_values=None):
    """可视化不同k值的性能表现"""
    fig, axes = plt.subplots(1, 2 if mse_values is not None else 1, figsize=(15, 6))
    
    if mse_values is not None:
        # 分类准确率
        axes[0].plot(k_values, accuracies, 'bo-', linewidth=2, markersize=8)
        axes[0].set_xlabel('k值', fontsize=12)
        axes[0].set_ylabel('准确率', fontsize=12)
        axes[0].set_title('k值对分类准确率的影响', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xticks(k_values)
        
        # 回归MSE
        axes[1].plot(k_values, mse_values, 'ro-', linewidth=2, markersize=8)
        axes[1].set_xlabel('k值', fontsize=12)
        axes[1].set_ylabel('均方误差 (MSE)', fontsize=12)
        axes[1].set_title('k值对回归MSE的影响', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].set_xticks(k_values)
        
        plt.suptitle('k-NN算法性能分析', fontsize=16, fontweight='bold')
    else:
        # 只有分类准确率
        if isinstance(axes, np.ndarray):
            ax = axes[0]
        else:
            ax = axes
        ax.plot(k_values, accuracies, 'bo-', linewidth=2, markersize=8)
        ax.set_xlabel('k值', fontsize=12)
        ax.set_ylabel('准确率', fontsize=12)
        ax.set_title('k值对分类准确率的影响', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_values)
    
    plt.tight_layout()
    plt.show()

def demo_classification():
    """k-NN分类示例"""
    print("=" * 50)
    print("k-NN分类算法演示")
    print("=" * 50)
    
    # 生成分类数据集
    X, y = make_classification(n_samples=200, n_features=2, n_redundant=0, 
                             n_informative=2, n_clusters_per_class=1, 
                             random_state=42)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 数据标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 测试不同的k值
    k_values = [1, 3, 5, 7, 9]
    accuracies = []
    
    print("不同k值的分类性能:")
    print("-" * 30)
    
    for k in k_values:
        # 创建并训练模型
        knn = KNearestNeighbors(k=k, distance_metric='euclidean')
        knn.fit(X_train_scaled, y_train)
        
        # 预测
        y_pred = knn.predict(X_test_scaled)
        
        # 计算准确率
        accuracy = calculate_accuracy(y_test, y_pred)
        accuracies.append(accuracy)
        print(f"k={k}: 准确率 = {accuracy:.4f}")
    
    # 可视化k值性能
    plot_k_performance(k_values, accuracies)
    
    # 使用最佳k值进行详细分析
    best_k = 5
    knn_best = KNearestNeighbors(k=best_k, distance_metric='euclidean')
    knn_best.fit(X_train_scaled, y_train)
    y_pred_best = knn_best.predict(X_test_scaled)
    
    print(f"\n使用k={best_k}的详细结果:")
    print(f"测试集准确率: {calculate_accuracy(y_test, y_pred_best):.4f}")
    
    # 预测概率
    y_proba = knn_best.predict_proba(X_test_scaled[:5])
    print(f"\n前5个测试样本的预测概率:")
    for i, proba in enumerate(y_proba):
        print(f"样本{i+1}: 类别0概率={proba[0]:.3f}, 类别1概率={proba[1]:.3f}")
    
    # 可视化分类结果
    plot_classification_results(X_train_scaled, y_train, X_test_scaled, y_test, y_pred_best, 
                               title=f"k-NN分类结果 (k={best_k})")

def demo_regression():
    """k-NN回归示例"""
    print("\n" + "=" * 50)
    print("k-NN回归算法演示")
    print("=" * 50)
    
    # 生成回归数据集
    X, y = make_regression(n_samples=200, n_features=1, noise=10, random_state=42)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 测试不同的k值
    k_values = [1, 3, 5, 7, 9]
    mse_values = []
    
    print("不同k值的回归性能:")
    print("-" * 30)
    
    for k in k_values:
        # 创建并训练模型
        knn = KNearestNeighbors(k=k, distance_metric='euclidean')
        knn.fit(X_train, y_train)
        
        # 预测
        y_pred = knn.predict(X_test)
        
        # 计算均方误差
        mse = calculate_mse(y_test, y_pred)
        mse_values.append(mse)
        print(f"k={k}: MSE = {mse:.2f}")
    
    # 可视化k值对MSE的影响
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, mse_values, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('k值', fontsize=12)
    plt.ylabel('均方误差 (MSE)', fontsize=12)
    plt.title('k值对回归MSE的影响', fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.xticks(k_values, fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.show()
    
    # 可视化回归结果
    best_k = 5
    knn_best = KNearestNeighbors(k=best_k, distance_metric='euclidean')
    knn_best.fit(X_train, y_train)
    y_pred_best = knn_best.predict(X_test)
    
    plt.figure(figsize=(12, 8))
    plt.scatter(X_train, y_train, alpha=0.6, label='训练数据', s=50, color='blue')
    plt.scatter(X_test, y_test, alpha=0.6, label='测试真实值', s=50, color='green')
    plt.scatter(X_test, y_pred_best, alpha=0.8, label=f'k-NN预测 (k={best_k})', s=50, color='red')
    plt.xlabel('特征值', fontsize=12)
    plt.ylabel('目标值', fontsize=12)
    plt.title('k-NN回归结果对比', fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # 设置坐标轴刻度
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # 添加性能指标文本
    mse_best = calculate_mse(y_test, y_pred_best)
    plt.text(0.02, 0.98, f'MSE: {mse_best:.2f}', transform=plt.gca().transAxes, 
             fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def demo_distance_metrics():
    """不同距离度量方法的比较"""
    print("\n" + "=" * 50)
    print("不同距离度量方法比较")
    print("=" * 50)
    
    # 生成数据
    X, y = make_classification(n_samples=150, n_features=2, n_redundant=0, 
                             n_informative=2, n_clusters_per_class=1, 
                             random_state=42)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 数据标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    distance_metrics = ['euclidean', 'manhattan', 'minkowski']
    
    print("不同距离度量的性能比较 (k=5):")
    print("-" * 40)
    
    for metric in distance_metrics:
        knn = KNearestNeighbors(k=5, distance_metric=metric, p=3)
        knn.fit(X_train_scaled, y_train)
        y_pred = knn.predict(X_test_scaled)
        accuracy = calculate_accuracy(y_test, y_pred)
        print(f"{metric:12s}: 准确率 = {accuracy:.4f}")

if __name__ == "__main__":
    print("k-最近邻算法 (k-NN) 完整实现和演示")
    print("=" * 60)
    
    # 运行分类演示
    demo_classification()
    
    # 运行回归演示
    demo_regression()
    
    # 运行距离度量比较
    demo_distance_metrics()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    
    # 使用说明
    print("\n使用说明:")
    print("1. 创建KNearestNeighbors实例")
    print("2. 使用fit()方法训练模型")
    print("3. 使用predict()方法进行预测")
    print("4. 对于分类任务，可以使用predict_proba()获取概率")
    
    print("\n示例代码:")
    print("knn = KNearestNeighbors(k=3)")
    print("knn.fit(X_train, y_train)")
    print("predictions = knn.predict(X_test)")
