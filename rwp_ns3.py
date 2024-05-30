import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import poisson
from matplotlib.patches import Circle

class RandomWaypointMobilityModel:
    def __init__(self, area_size, lambda_poisson, r_cs, min_speed=3, max_speed=8, pause_time=2.0):
        """
        初始化随机航点移动模型
        :param area_size: 移动区域的边长
        :param lambda_poisson: 泊松过程的强度（每单位面积的平均点数）
        :param min_speed: 最小速度 (m/s)
        :param max_speed: 最大速度 (m/s)
        :param pause_time: 暂停时间 (秒)
        """
        self.area_size = area_size
        self.lambda_poisson = lambda_poisson
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.pause_time = pause_time
        self.radius_cs = r_cs
        self.n_points = self._get_poisson_number(area_size**2 * lambda_poisson)
        self.positions = np.random.rand(self.n_points, 2) * area_size
        self.destinations = np.zeros((self.n_points, 2))
        self.velocities = np.zeros((self.n_points, 2))
        self.pause_counters = np.zeros(self.n_points)

    def _get_poisson_number(self, mean):
        """
        根据泊松分布生成点的数量
        """
        return poisson.rvs(mean)

    def begin_walks(self):
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
                # print(self.positions[i])

    def update_positions(self, dt):
        self.positions += self.velocities * dt
        for i in range(self.n_points):
            # print(f'des: {self.destinations[i]},\tpos: {self.positions[i]},\tv: {self.velocities[i]}')
            if np.dot(self.destinations[i] - self.positions[i], self.velocities[i]) < 0:
                self.destinations[i] = np.zeros(2)
                self.velocities[i] = np.zeros(2)
                self.pause_counters[i] = self.pause_time

def update(frame_num, model, scatter, circles):
    model.begin_walks()
    model.update_positions(0.1)
    scatter.set_offsets(model.positions)
    # Update circles positions
    for i, circle in enumerate(circles):
        circle.center = model.positions[i]

# 设置模拟参数
area_size = 5000  # 区域边长
lambda_poisson = 0.000002  # 每平方米的平均点数
min_speed = 3  # 最小速度
max_speed = 50  # 最大速度
pause_time = 20  # 暂停时间
radius_cs = 800 # 载波侦听半径

# 创建模型和动画
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)

model = RandomWaypointMobilityModel(area_size, lambda_poisson, radius_cs, min_speed, max_speed, pause_time)
scatter = ax.scatter(model.positions[:, 0], model.positions[:, 1])

# 初始化圆环
circles = [Circle(model.positions[i], radius_cs, color='blue', fill=False) for i in range(model.n_points)]
for circle in circles:
    ax.add_patch(circle)

anim = FuncAnimation(fig, update, fargs=(model, scatter, circles), frames=200, interval=10)

plt.show()
