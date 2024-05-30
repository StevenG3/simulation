import simpy
import random
import math

class Message:
    def __init__(self, content, sender_id):
        self.content = content
        self.sender_id = sender_id

class Node:
    def __init__(self, env, node_id, cell_id, shared_queue, state='I'):
        self.env = env
        self.node_id = node_id
        self.cell_id = cell_id
        self.shared_queue = shared_queue  # 共享队列
        self.state = state
        self.env.process(self.node_process())

    def node_process(self):
        while True:
            # 检查共享队列中的消息
            if not self.shared_queue.items:
                yield self.env.timeout(1)  # 如果队列为空，则等待一个时间单位
                continue
            
            # 获取并处理所有队列中的消息
            while self.shared_queue.items:
                msg = yield self.shared_queue.get()
                if msg.sender_id != self.node_id:  # 避免处理自己发送的消息
                    # 根据消息更新状态...
                    print(f"Node {self.node_id} received a message from Node {msg.sender_id} at time {self.env.now}")
                    self.state = 'S'  # 示例：收到消息后更新状态为'S'

            # 如果节点处于B状态，则广播消息
            if self.state == 'B':
                self.broadcast(Message("Hello from " + str(self.node_id), self.node_id))
                yield self.env.timeout(1)  # 广播后等待一个时间单位

            if self.state == 'I':
                msg = yield self.inbox.get()  # 监听消息
                if msg.sender_id == self.cell_id:
                    self.state = 'S'
                else:
                    self.state = 'A'
                    self.message = Message(msg.content, self.cell_id)
            elif self.state == 'A':
                yield self.env.timeout(c * c)  # 等待c * c slots
                if random.random() < p:  # 以概率p发送消息
                    self.broadcast(self.message)
                self.time_listened += 1
                if self.time_listened == k * (math.log(n) + math.log(R)):
                    self.state = 'B'
            elif self.state == 'S':
                yield self.env.timeout(1)  # 状态S不执行任何操作
            else:
                break  # 如果状态未知，则退出循环

    def broadcast(self, message):
        print(f"Node {self.node_id} broadcasting message at time {self.env.now}")
        self.shared_queue.put(message)

# 创建SimPy环境和共享队列
env = simpy.Environment()
shared_queue = simpy.Store(env)

# 初始化节点，包括一个处于B状态的源节点
nodes = [Node(env, i, i, shared_queue, 'B' if i == 0 else 'I') for i in range(5)]

# 运行仿真
env.run(until=10)
