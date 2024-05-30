import numpy as np
import matplotlib.pyplot as plt
import random
import time

# 固定随机种子以便结果可复现
# random.seed(42)
# np.random.seed(42)
random.seed(time.time())

# 定义矩形区域大小和泊松点过程参数
xMin, xMax, yMin, yMax = 0, 5000, 0, 5000
lambda0 = 0.00001  # 强度参数调整为每单位面积的平均点数
areaTotal = (xMax - xMin) * (yMax - yMin)

# 定义感染半径
R_cs = 1000

# 初始化记录
p_values = np.arange(0.1, 1.05, 0.05)
efficiency_indices = []  # 存储每个p下的归一化效率指标
valid_p_values = []  # 存储感染率达到100%的p值

# 模拟函数
def simulate(p):
    numbPoints = np.random.poisson(lambda0 * areaTotal)
    xx = np.random.uniform(xMin, xMax, numbPoints)
    yy = np.random.uniform(yMin, yMax, numbPoints)
    node_states = np.zeros(numbPoints, dtype=int)
    initial_infection_index = random.randint(0, numbPoints - 1)
    node_states[initial_infection_index] = 1
    infected_by_round = {0: {initial_infection_index}}
    flows = 0
    rounds = 0
    is_infection_ended = False

    while not is_infection_ended:
        new_infections = set()
        if rounds in infected_by_round:
            for i in infected_by_round[rounds]:
                infection_chance = 1 if rounds == 0 else p  # 第一轮感染不受概率 p 影响
                if np.random.rand() <= infection_chance:
                    for j in range(numbPoints):
                        if np.linalg.norm(np.array([xx[i], yy[i]]) - np.array([xx[j], yy[j]])) <= R_cs:
                            flows += 1
                            if node_states[j] == 0:
                                node_states[j] = 1
                                new_infections.add(j)
        if new_infections:
            infected_by_round[rounds + 1] = new_infections
            rounds += 1
        else:
            is_infection_ended = True
    infection_rate = np.mean(node_states)
    return flows, rounds, infection_rate

# 对每个p值进行模拟并记录结果
for p in p_values:
    flows, rounds, infection_rate = simulate(p)
    if infection_rate == 1.0:  # 只有当感染率为100%时
        valid_p_values.append(p)
        efficiency_indices.append((flows, rounds))

# 计算归一化效率指标
if efficiency_indices:
    max_flows = max(efficiency_indices, key=lambda x: x[0])[0]
    max_rounds = max(efficiency_indices, key=lambda x: x[1])[1]
    normalized_efficiency = [(flows * rounds) / (max_flows * max_rounds) for flows, rounds in efficiency_indices]

    # 绘制归一化效率指标图
    plt.figure(figsize=(10, 6))
    plt.plot(valid_p_values, normalized_efficiency, marker='o', linestyle='-', color='purple')
    plt.title('Normalized Efficiency Indicator vs. Infection Probability (100% Infection Rate Only)')
    plt.xlabel('Infection Probability (p)')
    plt.ylabel('Normalized Efficiency Indicator')
    plt.grid(True)
    plt.show()
else:
    print("No simulations resulted in a 100% infection rate.")
