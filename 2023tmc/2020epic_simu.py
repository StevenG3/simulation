# Epidemic and Timer-Based Message Dissemination in VANETs: A Performance Comparison
# Author: Pietro Spadaccino, Francesca Cuomo, and Andrea Baiocchi

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import time
import copy

# Parameters 
# input
# D = {150, 200, 250, 300}
D = 15
n = 100
R = 3
R_min = 3
alpha = 0.3

# 设置随机种子以便结果可复现
# random.seed(time.time())
# 设置固定的随机种子
random.seed(42)  # 对于 Python 的 random 模块
np.random.seed(42)  # 对于 numpy 的随机函数

# 3. 初始化节点
class Node:
    def __init__(self, id, x, y, state='S', message=None):
        self.id = id
        self.x = x
        self.y = y
        self.state = state
        self.message = message
        self.rcv_messages = []
        self.timer = 0
        self.T_max = 0
        self.T_min = 0
        self.nbrs = set()
    
    # 节点每个时间单位的处理，定义返回值为state，表示节点的状态
    def on_message_receipt(self, msg, slot=0):
        print(f"Node {self.id} with state {self.state}")
        self.T_max = slot
        if self.state == 'R':
            pass
        elif self.state == 'S':
            self.rcv_messages = [msg]
            self.timer = slot + max(self.T_min, self.T_max * np.ceil(1 - simu.distance[msg.id][self.id] / R))
            self.state = 'I'
        elif self.state == 'I':
            self.rcv_messages.append(msg)

        self.rev_slot = slot

    def evaluate_positions(self):
        not_reached = self.nbrs.copy()
        # emitters = {msg.id for msg in self.rcv_messages}
        # 将所有的msg.emitters合并到一个集合中
        emitters = set()
        for msg in self.rcv_messages:
            emitters.update(msg.emitters)

        for emitter in emitters:
            for nbr in list(not_reached):
                if simu.distance[nbr][emitter] < R_min:
                    not_reached.remove(nbr)

        return len(not_reached) > alpha * len(self.nbrs)
    
    def on_timeout(self):
        do_relay = self.evaluate_positions()

        # 如果有消息需要转发，则发送消息；否则使用接收到的消息
        # 先除去当前slot收到的消息，再取最后一个消息
        while self.rcv_messages and self.rcv_messages[-1].slot == simu.slot:
            print(f"Node {self.id} remove message, msg id: {self.rcv_messages[-1].id} ttl: {self.rcv_messages[-1].ttl}, slot: {self.rcv_messages[-1].slot}")
            self.rcv_messages.pop()

        msg = self.rcv_messages[-1] if self.rcv_messages else self.message
        print(f"Node {self.id} timeout")
        if msg: 
            if do_relay and msg.ttl > 0:
                msg = self.update_message(msg)
                self.relay_message(msg)
            self.state = 'R'
        else:
            print(f"Node {self.id} timeout, no message to relay, error with timer")
        
    def update_message(self, msg):
        msg.id = self.id
        msg.emitters.append(self.id)
        msg.ttl -= 1
        msg.slot = simu.slot
        return msg

    def relay_message(self, msg):
        print(f"Node {self.id} relay message, msg id: {msg.id} ttl: {msg.ttl} msg slot: {msg.slot}")
        for i in range(n):
            if self.id != i and simu.distance[self.id][i] < R:
                print(f"from {self.id} to {i}")
                simu.rcv_set[i] = msg

    def node_process(self, slot, rcv_set):
        # 如果节点在rcv_set中，说明在上一个slot中收到了消息，其中rsv_set中是key: id, value: message的形式
        print(f"timer {self.timer} slot {slot} state {self.state}")
        if self.timer <= slot and self.state == 'I':
            self.on_timeout()
        elif self.id in rcv_set:
            self.on_message_receipt(rcv_set[self.id], slot)
            rcv_set.pop(self.id)

        return self.state
        
class Message:
    def __init__(self, id):
        self.id = id
        self.emitters = [id]
        self.ttl = 5
        self.slot = 0

class Simu:
    def __init__(self, ax):
        self.ax = ax
        self.slot = 0
        self.nodes = [Node(i, random.uniform(0, D), random.uniform(0, D), 'S') for i in range(n)]
        self.nodes[0].state = 'I'  # 设定第一个节点为广播节点
        self.nodes[0].message = Message(0)
        self.init_distance()
        # calc nbrs of node
        for i in range(n):
            for j in range(n):
                if i != j and self.distance[i][j] < R:
                    self.nodes[i].nbrs.add(j)
        # 以key: id, value: message的形式存储节点收到的消息
        self.rcv_set = {}

        # 以key:state, value: nodes的形式存储节点
        # nodes的存储方式以set的形式存储，方便节点的增删
        self.state_nodes = {'I': set(), 'S': set(), 'R': set()}
        self.new_nodes = {'I': set(), 'S': set(), 'R': set()}
        for node in self.nodes:
            self.state_nodes[node.state].add(node.id)

        self.annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
    
    # def init_nodes(self):
    #     x0, y0 = random.uniform(0, D), random.uniform(0, D)
    #     self.nodes.append(Node(0, x0, y0, 'B', Message('0', 0, c0)))
    #     for i in range(1, n):
    #         self.nodes.append(Node(i, random.uniform(0, D), random.uniform(0, D), 'I'))
    
    def init_distance(self):
        self.distance = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                self.distance[i][j] = np.sqrt((self.nodes[i].x - self.nodes[j].x) ** 2 + (self.nodes[i].y - self.nodes[j].y) ** 2)

    def update_annot(self, node):
        self.annot.xy = (node.x, node.y)
        text = f"ID: {node.id}\nState: {node.state}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)
        self.annot.set_visible(True)  # 确保每次都设置为可见
        self.ax.figure.canvas.draw_idle()  # 立即重新绘制图形
        print(f"Node {node.id} at ({node.x:.2f}, {node.y:.2f}) state {node.state}")

    def hover(self, event):
       if event.inaxes == self.ax:
            vis = self.annot.get_visible()
            for node in self.nodes:
                if np.linalg.norm([event.xdata - node.x, event.ydata - node.y]) <= 0.1:  # 确保触发距离适当
                    self.update_annot(node)
                    self.annot.set_visible(True)
                    self.ax.figure.canvas.draw_idle()
                    return
            if vis:
                self.annot.set_visible(False)
                self.ax.figure.canvas.draw_idle()

    def process_node(self, node_id):
        """处理单个节点状态转换并更新状态字典"""
        state = self.nodes[node_id].node_process(self.slot, self.rcv_set)
        self.new_nodes[state].add(node_id)

        return state

    # 可视化
    # 处于不同状态的节点使用不同的颜色表示
    def visualize(self):
        self.ax.clear()
        self.ax.set_xlim(0, D)
        self.ax.set_ylim(0, D)
        colors = {'I': 'red', 'S': 'blue', 'R': 'orange'}
        for node in self.nodes:
            self.ax.scatter(node.x, node.y, color=colors[node.state])
        plt.draw()

    # 运行模拟
    # 每次点击模拟一个slot，每个round有2 * c * c个slot
    def run(self):
        # 每次点击模拟一个slot
        for state in ['I', 'S', 'R']:
            for node_id in self.state_nodes[state]:
                cstate = self.process_node(node_id)
                self.new_nodes[cstate].add(node_id)

        self.state_nodes = copy.deepcopy(self.new_nodes)
        self.new_nodes = {'I': set(), 'S': set(), 'R': set()}

        self.slot += 1

        # 如果不移动，不需要下面的计算
        # for i in range(n):
        #     for j in range(i + 1, n):
        #         if i != j and self.distance[i][j] < R:
        #             self.nodes[i].nbrs.add(j)
        #             self.nodes[j].nbrs.add(i)

        # 打印每个状态的节点数量
        for state in ['I', 'S', 'R']:
            print(f"State {state}: {len(self.state_nodes[state])}")

        self.visualize()

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, D)
ax.set_ylim(0, D)
simu = Simu(ax)
simu.visualize()

def on_click(event):
    simu.run()

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect("motion_notify_event", simu.hover)

plt.show()