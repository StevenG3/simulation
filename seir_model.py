# 导入所需的库
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# SEIR模型方程
def SEIR_model(y, t, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I
    dEdt = beta * S * I - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# 初始条件
S0 = 0.99
E0 = 0.01
I0 = 0.00
R0 = 0.00
y0 = [S0, E0, I0, R0]

# 参数
beta = 0.3   # 传染率
sigma = 0.1  # 潜伏期转化为感染期的速率
gamma = 0.05 # 感染者恢复速率

# 时间向量
t = np.linspace(0, 200, 200)

# 解SEIR模型方程
solution = odeint(SEIR_model, y0, t, args=(beta, sigma, gamma))

# 提取结果
S, E, I, R = solution.T

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(t, S, label='Susceptible')
plt.plot(t, E, label='Exposed')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.xlabel('Time (days)')
plt.ylabel('Proportion of Population')
plt.title('SEIR Model Simulation')
plt.legend()
plt.grid(True)
plt.show()
