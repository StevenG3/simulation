import numpy as np
import matplotlib.pyplot as plt
import random
import time

# 固定随机种子以便结果可复现
# random.seed(42)
# np.random.seed(42)
# 设置随机种子以便结果可复现
random.seed(time.time())

# 定义矩形区域大小和泊松点过程参数
xMin, xMax, yMin, yMax = 0, 5000, 0, 5000
lambda0 = 0.00001
areaTotal = (xMax - xMin) * (yMax - yMin)

# 定义感染半径
R_cs = 1000

# 初始化记录
p_values = np.arange(0.1, 1.05, 0.05)  # 不同的感染概率p
flows_per_p = []  # 每个p值对应的总流量
rounds_per_p = []  # 每个p值对应的最终感染轮数

# 主模拟函数
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

    return flows, rounds

# 对每个p值进行模拟并记录结果
for p in p_values:
    flows, rounds = simulate(p)
    flows_per_p.append(flows)
    rounds_per_p.append(rounds)

# -------------- 绘制rounds/flows关于p的变化图（一张图） -------------------- #
'''
# 绘制曲线图
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Infection Probability (p)')
ax1.set_ylabel('Total Flows', color=color)
ax1.plot(p_values, flows_per_p, marker='o', linestyle='-', color=color, label='Total Flows')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # 实例化一个第二个y轴
color = 'tab:blue'
ax2.set_ylabel('Final Rounds', color=color)
ax2.plot(p_values, rounds_per_p, marker='x', linestyle='--', color=color, label='Final Rounds')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # 为了适应第二个y轴
plt.title('Total Flows and Final Rounds vs. Infection Probability')
plt.show()
'''

# -------------- 绘制rounds/flows关于p的变化图（一张图） -------------------- #
# 创建纵向排列的两个图，分别展示Total Flows和Final Rounds关于Infection Probability的变化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 绘制Total Flows关于Infection Probability的变化
color_flows = 'tab:red'
ax1.set_xlabel('Infection Probability (p)')
ax1.set_ylabel('Total Flows', color=color_flows)
ax1.plot(p_values, flows_per_p, marker='o', linestyle='-', color=color_flows)
ax1.tick_params(axis='y', labelcolor=color_flows)
ax1.set_title('Total Flows vs. Infection Probability')

# 绘制Final Rounds关于Infection Probability的变化
color_rounds = 'tab:blue'
ax2.set_xlabel('Infection Probability (p)')
ax2.set_ylabel('Final Rounds', color=color_rounds)
ax2.plot(p_values, rounds_per_p, marker='x', linestyle='--', color=color_rounds)
ax2.tick_params(axis='y', labelcolor=color_rounds)
ax2.set_title('Final Rounds vs. Infection Probability')

plt.tight_layout()
plt.show()

# -------------- 绘制归一化效率指标关于p的变化图 -------------------- #
'''
# 计算归一化效率指标
max_flows = max(flows_per_p)
max_rounds = max(rounds_per_p)
efficiency_per_p = [(rounds * flows) / (max_rounds * max_flows) for rounds, flows in zip(rounds_per_p, flows_per_p)]

# 绘制归一化效率指标图
plt.figure(figsize=(10, 6))
plt.plot(p_values, efficiency_per_p, marker='o', linestyle='-', color='purple')
plt.title('Normalized Efficiency Indicator vs. Infection Probability')
plt.xlabel('Infection Probability (p)')
plt.ylabel('Normalized Efficiency Indicator')
plt.grid(True)
plt.show()
'''