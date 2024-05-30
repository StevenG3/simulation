import numpy as np
import matplotlib.pyplot as plt

# 初始化参数
num_nodes = 10  # 节点数
area_size = (100, 100)  # 区域大小
max_speed = 5  # 最大速度
sim_time = 100  # 模拟时间

# 初始化节点位置
node_positions = np.random.rand(num_nodes, 2) * area_size

# 用于存储节点的路径
paths = [[] for _ in range(num_nodes)]

# 模拟移动
for _ in range(sim_time):
    for i in range(num_nodes):
        if not paths[i] or np.array_equal(paths[i][-1], node_positions[i]):
            # 选择一个新的随机目的地
            destination = np.random.rand(2) * area_size
            paths[i].append(destination)
        else:
            # 向目的地移动
            direction = paths[i][-1] - node_positions[i]
            distance = np.linalg.norm(direction)
            step_size = min(max_speed, distance)  # 确保不会超过目的地
            step_direction = direction / distance
            node_positions[i] += step_direction * step_size

# 绘制路径
plt.figure(figsize=(8, 8))
for i in range(num_nodes):
    if paths[i]:
        path = np.array(paths[i])
        plt.plot(path[:, 0], path[:, 1], marker='o')
    plt.plot(node_positions[i, 0], node_positions[i, 1], 'kx')  # 绘制当前位置

plt.xlim(0, area_size[0])
plt.ylim(0, area_size[1])
plt.title('Random Waypoint Model Simulation')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
