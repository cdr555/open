import torch

# # 创建一个2x3的张量
# tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])

# # # 使用 torch.transpose 进行转置
# # transposed_tensor = torch.transpose(tensor, 0, 1)
# # .T 方法适用于二维张量，交换两个维度
# transposed_tensor = tensor.T

# print(tensor)
# print(transposed_tensor)


# 创建一个3维张量
tensor = torch.randn(2, 3, 4)

# 交换第0维和第1维
transposed_tensor = tensor.transpose(0, 1)
print(transposed_tensor.shape)  