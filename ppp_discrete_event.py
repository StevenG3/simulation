import numpy as np
import simpy

# 定义感染模型
class InfectionModel:
    def __init__(self, env, lambda0, areaTotal, R_cs):
        self.env = env
        self.lambda0 = lambda0
        self.areaTotal = areaTotal
        self.R_cs = R_cs
        self.numbPoints = np.random.poisson(lambda0 * areaTotal)
        self.xx = np.random.uniform(xMin, xMax, self.numbPoints)
        self.yy = np.random.uniform(yMin, yMax, self.numbPoints)
        self.node_states = np.zeros(self.numbPoints, dtype=int)
        self.node_states[0] = 1  # 假设第一个节点初始感染

    def infect_nodes(self):
        while True:
            new_infections = False
            for i in range(self.numbPoints):
                if self.node_states[i] == 1:  # 对于每个已感染节点
                    for j in range(self.numbPoints):
                        if self.node_states[j] == 0 and np.linalg.norm(np.array([self.xx[i], self.yy[i]]) - np.array([self.xx[j], self.yy[j]])) <= self.R_cs:
                            self.node_states[j] = 1  # 感染易感节点
                            new_infections = True
            if not new_infections:
                break
            yield self.env.timeout(1)  # 模拟时间进展

# 模拟设置
env = simpy.Environment()
xMin, xMax = 0, 5000
yMin, yMax = 0, 5000
areaTotal = (xMax - xMin) * (yMax - yMin)
lambda0 = 0.00000256
R_cs = 1000

# 创建感染模型实例并开始模拟
model = InfectionModel(env, lambda0, areaTotal, R_cs)
env.process(model.infect_nodes())
env.run()

# 打印模拟结果
infection_rate = np.sum(model.node_states) / model.numbPoints
print(f"Simulation ended. Total points: {model.numbPoints}, Infection rate: {infection_rate:.2%}.")
