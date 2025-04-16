import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

def grunwald_letnikov_coefficient(beta, k):
    """计算Grünwald-Letnikov广义二项式系数 C(β, k)"""
    coeff = 1.0
    for i in range(1, k+1):
        coeff *= (-1) * (beta - i + 1) / i
    return coeff

# 参数设置
E = 10e6          # 弹性模量 (Pa)
eta = 100e3       # 粘性系数 (Pa·s^β)
beta = 0.7        # 分数阶导数阶数（粘性流动速率）
sigma0 = 5e6      # 施加的恒定应力 (Pa)
t_max = 100       # 最大时间 (s)
dt = 0.01         # 时间步长 (s)，减小步长以提高精度和平滑度
n_steps = int(t_max / dt) + 1

# 初始化时间序列和应变数组
t = np.linspace(0, t_max, n_steps)
epsilon = np.zeros(n_steps)
# 设置初始条件
epsilon[0] = 0

# Grünwald-Letnikov数值求解分数阶微分方程
# 方程：sigma0 = E * epsilon(t) + eta * d^beta epsilon/dt^beta
for n in range(1, n_steps):
    # 计算分数阶导数项 d^beta epsilon/dt^beta 的近似值
    d_beta = 0.0
    for k in range(n+1):
        coeff = grunwald_letnikov_coefficient(beta, k)
        if n-k >= 0:  # 确保索引有效
            d_beta += coeff * epsilon[n-k]
    d_beta *= (1.0 / (dt ** beta))
    
    # 解方程：sigma0 = E * epsilon[n] + eta * d_beta
    epsilon[n] = (sigma0 - eta * d_beta) / E

# 传统Kelvin-Voigt模型的解析解
epsilon_classic = (sigma0 / E) * (1 - np.exp(-E * t / eta))

# 绘图
plt.figure(figsize=(10, 6), dpi=100)
# 使用更高平滑度绘制曲线
plt.plot(t, epsilon_classic, '-', color='gray', linewidth=2.5, label='传统模型', alpha=0.9)
plt.plot(t, epsilon, '-', color='red', linewidth=2.5, label=f'分数阶模型 (β={beta})', alpha=0.9)
# 使曲线更平滑
plt.grid(True, linestyle=':', alpha=0.7)
plt.xlim(0, t_max)
plt.ylim(0, sigma0 / E * 1.1)
plt.xlabel('时间 t (s)', fontsize=12)
plt.ylabel('应变 ε(t)', fontsize=12)
plt.title('蠕变响应对比：数值积分法实现', fontsize=14)
plt.legend(fontsize=12)

# 标注
classic_y = epsilon_classic[int(len(t)*0.2)]  # 20%处的传统模型值
fractional_y = epsilon[int(len(t)*0.6)]  # 60%处的分数阶模型值

plt.annotate('传统模型：指数衰减至稳态', 
             xy=(t_max*0.2, classic_y), 
             xytext=(t_max*0.3, classic_y*0.7), 
             arrowprops=dict(arrowstyle="->", color='gray', lw=1.5))
plt.annotate('分数阶模型：幂律衰减', 
             xy=(t_max*0.6, fractional_y), 
             xytext=(t_max*0.4, fractional_y*0.8), 
             arrowprops=dict(arrowstyle="->", color='red', lw=1.5))

plt.tight_layout()
plt.show()