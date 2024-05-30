import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from scipy.spatial.distance import cdist

class RandomWaypointMobilityModel:
    def __init__(self, area_size, lambda_poisson, r_cs, p_infection=1.0, min_speed=3, max_speed=8, pause_time=2.0):
        self.area_size = area_size
        self.lambda_poisson = lambda_poisson
        self.radius_cs = r_cs
        self.p_infection = p_infection
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.pause_time = pause_time
        self.infect_points = 1
        self.rounds = 0
        self.n_points = np.random.poisson(area_size**2 * lambda_poisson)
        self.positions = np.random.rand(self.n_points, 2) * area_size
        self.destinations = np.zeros((self.n_points, 2))
        self.velocities = np.zeros((self.n_points, 2))
        self.pause_counters = np.zeros(self.n_points)
        self.infected = np.zeros(self.n_points, dtype=bool)
        self.infected[np.random.randint(self.n_points)] = True  # 随机选择一个节点作为初始感染节点

    def update_positions(self, dt):
        if self.infect_points < self.n_points:
            self.rounds += 1
            print(f'interval rounds: {self.rounds}')
        for i in range(self.n_points):
            if self.pause_counters[i] <= 0:
                self.destinations[i] = np.random.rand(2) * self.area_size
                direction = self.destinations[i] - self.positions[i]
                distance = np.linalg.norm(direction)
                speed = np.random.uniform(self.min_speed, self.max_speed)
                self.velocities[i] = direction / distance * speed
                self.pause_counters[i] = self.pause_time
            elif np.linalg.norm(self.velocities[i]) == 0:
                self.pause_counters[i] -= 1

        self.positions += self.velocities * dt

        # 检查是否到达目的地
        for i in range(self.n_points):
            if np.dot(self.destinations[i] - self.positions[i], self.velocities[i]) < 0:
                self.destinations[i] = np.zeros(2)
                self.velocities[i] = np.zeros(2)
                self.pause_counters[i] = self.pause_time

        # 感染逻辑
        self.spread_infection()

    def spread_infection(self):
        for i in range(self.n_points):
            if self.infected[i]:
                for j in range(self.n_points):
                    if not self.infected[j] and np.random.rand() <= self.p_infection:
                        distance = np.linalg.norm(self.positions[i] - self.positions[j])
                        if distance <= self.radius_cs:
                            self.infected[j] = True
                            self.infect_points += 1

    def infect_rounds(self):
        return self.rounds

def update(frame_num, model, scatter, circles):

    model.update_positions(0.1)
    scatter.set_offsets(model.positions)
    scatter.set_array(np.where(model.infected, 1, 0))  # 更新颜色，根据是否感染
    for i, circle in enumerate(circles):
        circle.center = model.positions[i]


# 设置模拟参数
area_size = 3000  # 区域边长
lambda_poisson = 0.000002  # 每平方米的平均点数
min_speed = 3  # 最小速度
max_speed = 50  # 最大速度
pause_time = 20  # 暂停时间
radius_cs = 1000 # 载波侦听半径

# 创建模型和动画
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)

model = RandomWaypointMobilityModel(area_size, lambda_poisson, radius_cs, p_infection=0.05, min_speed=min_speed, max_speed=max_speed, pause_time=pause_time)
scatter = ax.scatter(model.positions[:, 0], model.positions[:, 1], c=np.where(model.infected, 1, 0), cmap='coolwarm')

# 初始化圆环表示感染半径，但可能不需要在动画中显示
circles = []  # 可选：创建圆环以可视化感染范围

anim = FuncAnimation(fig, update, fargs=(model, scatter, circles), frames=200, interval=100)

plt.show()

print(f'infect rounds: {model.infect_rounds()}')
