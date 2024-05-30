# 导入所需的库
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# SIRS模型方程
def SIRS_model(y, t, beta, gamma, xi):
    S, I, R = y
    dSdt = -beta * S * I + xi * R
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I - xi * R
    return [dSdt, dIdt, dRdt]

# 初始条件
S0 = 0.99
I0 = 0.01
R0 = 0.00
y0 = [S0, I0, R0]

# 参数
beta = 0.3  # 传染率
gamma = 0.05 # 感染者恢复速率
xi = 0.01   # 恢复者失去免疫的速率，变回易感状态

# 时间向量
t = np.linspace(0, 200, 200)

# 解SIRS模型方程
solution = odeint(SIRS_model, y0, t, args=(beta, gamma, xi))

# 提取结果
S, I, R = solution.T

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.xlabel('Time (days)')
plt.ylabel('Proportion of Population')
plt.title('SIRS Model Simulation')
plt.legend()
plt.grid(True)
plt.show()
