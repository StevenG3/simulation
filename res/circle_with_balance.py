import matplotlib.pyplot as plt
import numpy as np
import random
import itertools

# 设置点的数量
num_points = 16
num_connections = 64  # 增加随机连接数目，以确保每个点都有线引出

# 生成圆上的等间距点
angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
points = np.array([(np.cos(angle), np.sin(angle)) for angle in angles])

# 定义三种浅颜色
colors = ['#FF9999', '#99FF99', '#FFFF99']

# 生成图形
plt.figure(figsize=(8, 8))

# 随机生成连接关系并使用三种浅颜色
connections = set()
while len(connections) < num_connections:
    i, j = random.sample(range(num_points), 2)
    if (i, j) not in connections and (j, i) not in connections:
        connections.add((i, j))

color_index = 0
for i, j in connections:
    point1 = points[i]
    point2 = points[j]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color=colors[color_index % len(colors)], linewidth=1.5)
    color_index += 1

# 标注每个点，用空心黑边的点表示
for point in points:
    plt.scatter(*point, color='white', edgecolor='black', s=100)  # 使用空心黑边的点表示点

# 指定的连接点序列
sequence = [11, 10, 0, 15]

# 绘制指定顺序的不封闭的连接线
for k in range(len(sequence) - 1):
    point1 = points[sequence[k]]
    point2 = points[sequence[k + 1]]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='green', linewidth=3)

# 隐藏轴和圆
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')

# 保存图形为JPG格式
plt.savefig('random_connections_with_mini_delay.jpg', format='jpg', bbox_inches='tight', pad_inches=0.1)
plt.show()
