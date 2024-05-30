import simpy
import numpy as np

# 定义状态常量
SUSCEPTIBLE = 'susceptible'
SEND = 'send'
RECV = 'recv'
INFECTED = 'infected'

class Individual:
    def __init__(self, env, index, state=SUSCEPTIBLE):
        self.env = env
        self.index = index
        self.state = state
        self.action = env.process(self.run())

    def run(self):
        # 初始状态为 SUSCEPTIBLE，等待被感染
        while True:
            yield self.env.timeout(1)  # 模拟等待，每次循环至少等待1个单位时间
            if self.state == RECV:
                # 进入 RECV 状态
                yield self.env.timeout(1)  # 模拟接受感染的时间
                self.state = SEND  # 转换到 SEND 状态
                print(f'Individual {self.index} is now in SEND state.')
            elif self.state == SEND:
                # 尝试感染其他个体
                yield self.env.timeout(1)  # 模拟尝试感染他人的时间
                self.state = INFECTED  # 成功感染后，转换到 INFECTED 状态
                print(f'Individual {self.index} is now INFECTED.')

def infect_individual(env, individual):
    yield env.timeout(0)  # 立即触发但保持生成器的形式
    if individual.state == SUSCEPTIBLE:
        individual.state = RECV
        print(f'Individual {individual.index} is now in RECV state.')

# 环境与个体初始化
env = simpy.Environment()
num_individuals = 5
individuals = [Individual(env, i) for i in range(num_individuals)]

# 模拟一个个体在模拟开始后被感染
env.process(infect_individual(env, individuals[0]))

env.run(until=10)
