import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        label = self.labels[idx]
        return sample, label

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 16 * 16, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(-1, 16 * 16 * 16)
        x = self.fc1(x)
        return x

# 示例数据
data = np.random.randn(1000, 3, 32, 32)  # 100个样本，每个样本是3x32x32的图像
labels = np.random.randint(0, 10, size=(1000,))  # 100个标签，范围在0到9之间

# 将数据转换为Tensor
data = torch.tensor(data, dtype=torch.float32)
labels = torch.tensor(labels, dtype=torch.long)

# 实例化数据集
dataset = CustomDataset(data, labels)

# 创建数据加载器
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

num_epochs = 10

for epoch in range(num_epochs):
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(train_loader):
        # 将梯度清零
        optimizer.zero_grad()

        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # 反向传播和优化
        loss.backward()
        optimizer.step()

        # 打印统计信息
        running_loss += loss.item()
        if i % 10 == 9:    # 每10个批次打印一次
            print(f'[Epoch {epoch + 1}, Batch {i + 1}] loss: {running_loss / 10:.3f}')
            running_loss = 0.0
        # if (epoch+1) % 10 == 0:
        #     print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print('Finished Training')