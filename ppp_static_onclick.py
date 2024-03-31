import numpy as np
import matplotlib.pyplot as plt
import random
import time

# 定义红色开始和结束的 ANSI 转义序列
RED_START = "\033[91m"
RED_END = "\033[0m"

# 设置随机种子以便结果可复现
random.seed(time.time())

# 定义矩形区域大小
xMin, xMax = 0, 5000
yMin, yMax = 0, 5000
areaTotal = (xMax - xMin) * (yMax - yMin)

# 泊松点过程参数
lambda0 = 0.00004  # 强度参数调整为每单位面积的平均点数
numbPoints = np.random.poisson(lambda0 * areaTotal)

# 定义感染半径（载波距离和感染距离）
R_cs = 1000
R_int = 1500

# 生成点的位置
xx = np.random.uniform(xMin, xMax, numbPoints)
yy = np.random.uniform(yMin, yMax, numbPoints)

# 初始化节点状态：0-易感(S), 1-感染(I)
node_states = np.zeros(numbPoints, dtype=int)

# 随机选择一个点作为初始感染源
initial_infection_index = random.randint(0, numbPoints - 1)
node_states[initial_infection_index] = 1

# 使用轮次作为键，节点索引作为值的结构来存储已感染的节点
infected_by_round = {0: {initial_infection_index}}

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xMin, xMax)
ax.set_ylim(yMin, yMax)

colors = ['blue' if state == 0 else 'red' for state in node_states]
scatter = ax.scatter(xx, yy, c=colors, edgecolors='k')

rounds = 0  # 记录感染过程进行的轮数
is_infection_ended = False  # 标记感染过程是否已结束

def infect_nodes(current_round):
    global node_states, infected_by_round
    new_infections = set()
    if current_round in infected_by_round:
        for i in infected_by_round[current_round]:
            for j in range(numbPoints):
                if node_states[j] == 0 and np.linalg.norm(np.array([xx[i], yy[i]]) - np.array([xx[j], yy[j]])) <= R_cs:
                    node_states[j] = 1  # 感染易感节点
                    new_infections.add(j)
    if new_infections:
        infected_by_round[current_round + 1] = new_infections
    return len(new_infections) > 0

def on_click(event):
    global rounds, is_infection_ended
    if not is_infection_ended:
        new_infection_occurred = infect_nodes(rounds)
        if new_infection_occurred:
            rounds += 1  # 只有当新的感染发生时才增加轮数
        else:
            is_infection_ended = True  # 没有新的感染发生，标记感染过程结束

        # 重新绘制图形以显示更新的状态
        colors = ['blue' if state == 0 else 'red' for state in node_states]
        scatter.set_facecolors(colors)
        fig.canvas.draw_idle()

        # 如果感染过程结束，打印感染率和总轮数
        if is_infection_ended:
            infection_rate = np.sum(node_states) / numbPoints
            print(f"Infection end. Total points: {RED_START}{numbPoints}{RED_END}, infection rate: {RED_START}{infection_rate:.2%}{RED_END}, total round: {RED_START}{rounds}{RED_END}.")

# 连接点击事件
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()

