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

# 生成点的位置
xx = np.random.uniform(xMin, xMax, numbPoints)
yy = np.random.uniform(yMin, yMax, numbPoints)

# 为每个点生成一个唯一 ID
point_ids = np.arange(numbPoints)

# 初始化节点状态：0-易感(S), 1-感染(I)
node_states = np.zeros(numbPoints, dtype=int)

# 将初始感染节点设置为0
initial_infection_index = 0
node_states[initial_infection_index] = 1

# 使用轮次作为键，节点索引作为值的结构来存储已感染的节点
infected_by_round = {0: {initial_infection_index}}

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xMin, xMax)
ax.set_ylim(yMin, yMax)

colors = ['blue' if state == 0 else 'red' for state in node_states]
scatter = ax.scatter(xx, yy, c=colors, edgecolors='k', picker=True)

# 添加注释以显示点的 ID
annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):
    pos = scatter.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = f"ID: {point_ids[ind['ind'][0]]}"
    annot.set_text(text)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

# 定义感染半径
R_cs = 1000  # 载波距离

rounds = 0  # 记录感染过程进行的轮数

def infect_nodes(current_round):
    global rounds, node_states, infected_by_round
    new_infections = set()
    if current_round in infected_by_round:
        for i in infected_by_round[current_round]:
            for j in range(numbPoints):
                if node_states[j] == 0 and np.linalg.norm(np.array([xx[i], yy[i]]) - np.array([xx[j], yy[j]])) <= R_cs:
                    node_states[j] = 1  # 感染易感节点
                    new_infections.add(j)
    if new_infections:
        rounds += 1
        infected_by_round[rounds] = new_infections
        return True
    return False

# 点击事件进行下一轮感染
def on_click(event):
    global rounds
    if infect_nodes(rounds):
        # 更新节点颜色以反映新的感染状态
        colors = ['blue' if state == 0 else 'red' for state in node_states]
        scatter.set_facecolors(colors)
        fig.canvas.draw_idle()
    else:
        infection_rate = np.sum(node_states) / numbPoints
        print(f"Infection process has ended. Total points: {RED_START}{numbPoints}{RED_END}, infection rate: {RED_START}{infection_rate:.2%}{RED_END}, total round: {RED_START}{rounds}{RED_END}.")

fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
