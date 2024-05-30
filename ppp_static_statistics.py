import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
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

# 定义感染半径
R_inf = 800

# 泊松点过程参数
lambda0 = 0.00000256  # 强度参数调整为每单位面积的平均点数
numbPoints = np.random.poisson(lambda0 * areaTotal)

# 生成点的位置
xx = np.random.uniform(xMin, xMax, numbPoints)
yy = np.random.uniform(yMin, yMax, numbPoints)

# 初始化节点状态：0-易感(S), 1-感染(I)
node_states = np.zeros(numbPoints, dtype=int)

# 将初始感染节点设置为0
initial_infection_index = 0
node_states[initial_infection_index] = 1

# 使用轮次作为键，节点索引作为值的结构来存储已感染的节点
infected_by_round = {0: {initial_infection_index}}

# 初始化感染统计
rounds = 0  # 记录感染过程进行的轮数
max_infection_rate = 0  # 最大感染率
max_infection_round = 0  # 达到最大感染率的轮数
start_time = time.time() * 1000  # 开始时间，转换为毫秒

def infect_nodes(current_round):
    global node_states, infected_by_round
    new_infections = set()
    if current_round in infected_by_round:
        for i in infected_by_round[current_round]:
            for j in range(numbPoints):
                if node_states[j] == 0 and np.linalg.norm(np.array([xx[i], yy[i]]) - np.array([xx[j], yy[j]])) <= R_inf:
                    node_states[j] = 1  # 感染易感节点
                    new_infections.add(j)
    if new_infections:
        infected_by_round[current_round + 1] = new_infections
    return len(new_infections) > 0

# 自动进行感染过程，直到没有新的感染发生
while infect_nodes(rounds):
    rounds += 1  # 每轮感染结束，轮数加一
    current_infection_rate = np.sum(node_states) / numbPoints
    if current_infection_rate > max_infection_rate:
        max_infection_rate = current_infection_rate
        max_infection_round = rounds

# 感染过程结束，统计结果
end_time = time.time() * 1000  # 结束时间，转换为毫秒
duration = end_time - start_time  # 计算达到最大感染率的时间，保留毫秒级别的精度

print(f"感染结束。总节点数：{RED_START}{numbPoints}{RED_END}, 最大感染率：{RED_START}{max_infection_rate:.2%}{RED_END}, 发生在第 {RED_START}{max_infection_round}{RED_END} 轮, 总感染轮数：{RED_START}{rounds}{RED_END}, 总耗时：{RED_START}{duration:.2f}{RED_END} 毫秒。")

# 绘图部分
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xMin, xMax)
ax.set_ylim(yMin, yMax)

colors = ['blue' if state == 0 else 'red' for state in node_states]
scatter = ax.scatter(xx, yy, c=colors, edgecolors='k', picker=True)  # 启用picker属性

# 创建一个注释对象，初始时不可见
annotation = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"),
                         arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

# 定义一个回调函数来处理鼠标悬停事件
def onpick(event):
    ind = event.ind[0]  # 获取选中点的索引，取第一个点
    point = event.artist  # 获取事件相关的艺术家对象，即散点图中的点
    x, y = point.get_offsets()[ind]  # 获取点的坐标
    annotation.xy = (x, y)  # 更新注释的位置
    text = f"ID: {ind}\nCoords: ({x:.2f}, {y:.2f})"
    annotation.set_text(text)  # 设置注释文本
    annotation.set_visible(True)  # 使注释可见
    fig.canvas.draw_idle()  # 重绘图形以显示注释

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()