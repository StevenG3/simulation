import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# 区域大小和密度参数
area_size = (4000, 4000)
lambda_param = 0.000008  # 节点的密度参数

# 计算区域面积
area = area_size[0] * area_size[1]

# 估算区域内的节点总数，这里用面积乘以密度来近似
num_nodes = int(area * lambda_param)

# 最大速度
max_speed = 5

# 模拟时间（动画帧数）
sim_time = 100

# 载波侦听半径
R_cs = 1000

# 随机初始化节点位置
node_positions = np.random.rand(num_nodes, 2) * area_size

# 随机初始化节点目的地
destinations = np.random.rand(num_nodes, 2) * area_size

# 初始化画布
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, area_size[0])
ax.set_ylim(0, area_size[1])

# 创建一个用于更新动画的函数
def update(frame):
    ax.clear()
    ax.set_xlim(0, area_size[0])
    ax.set_ylim(0, area_size[1])
    
    for i in range(num_nodes):
        # 向目的地移动
        direction = destinations[i] - node_positions[i]
        distance = np.linalg.norm(direction)
        if distance != 0:
            step_size = min(max_speed, distance)  # 确保不会超过目的地
            step_direction = direction / distance
            node_positions[i] += step_direction * step_size
        else:
            # 选择一个新的随机目的地
            destinations[i] = np.random.rand(2) * area_size
        
        # 绘制节点位置
        ax.scatter(node_positions[i, 0], node_positions[i, 1], c='blue')
        # 绘制以节点为中心的圆，颜色浅一些
        circle = Circle(node_positions[i], R_cs, color='green', fill=False, alpha=0.5)
        ax.add_patch(circle)
    
    # 重新绘制图形
    ax.set_title('Random Waypoint Model Simulation')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)

# 使用FuncAnimation创建动画
ani = FuncAnimation(fig, update, frames=sim_time, repeat=False)

plt.show()
