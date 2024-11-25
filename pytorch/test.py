import torch
import torch.nn as nn
import torch.optim as optim

# 生成一些示例数据
x = torch.randn(100, 1)  # 100 个样本，每个样本有 1 个特征
y = 3 * x + 2 + torch.randn(100, 1)  # 线性关系加上一些噪声

# 定义一个简单的线性回归模型
class LinearRegressionModel(nn.Module):
    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(1, 1)  # 输入 1 个特征，输出 1 个特征

    def forward(self, x):
        return self.linear(x)

model = LinearRegressionModel()

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 训练模型
num_epochs = 1000
for epoch in range(num_epochs):
    # 前向传播
    outputs = model(x)
    loss = criterion(outputs, y)

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# 打印模型参数
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.data)