# Jamming-Resilient Message Dissemination in Wireless Networks
# Authors: Yifei Zou , Member, IEEE, Dongxiao Yu, Senior Member, IEEE, and Fan Wu, Member, IEEE
# Date: 2023
# Description: This file is the simulation of the 2023 TMC paper. It is used to evaluate the performance of the proposed algorithm.
# parameters:
# D: a network area with diameter D
# n: number of nodes
# R: the network is connected with respect to distance R
# alpha: the path-loss exponent determined by the environment (2,6]
# beta: beta > 1 is a constant threshold determined by hardware of SINR
# P_min/P_max: P_min and P_max are the minimum and maximum transmission powers among all the nodes in the network,
# and P_max/P_min is assumed to be a constant.
# epsilon: A standard assumption is to set a tighter jamming threshold N, with epsilon being a positive constant,
# N: A standard assumption is to set a tighter jamming threshold N
# p: A node in state A first listens in the first c * c slots and then transmits message M_n with constant probability p
# c: c * c colors and 2 * c * c slots per round
# zeta: Regular Jamming (REGJ) with a constant probability zeta to jam the network at each round
# T_zeta: there are about T_zeta jamming rounds occured in our simulation

# Algorithm 1 presents the pseudo-code for our message dissemination algorithm. The process is divided into succes-
# sive rounds, with each consisting of 2*c*c slots. There are four states, namely I, A, B, and S for the nodes in the net-
# work. Nodes in different states have different operations at each round. We denote by Mu the message that contains
# the source message and the cell ID of node u.

# A node in state I means that the node is not ready to help deliver the source message M. Considering
# that nodes have the non-spontaneous wakeup assumption, only when receiving a message can the
# nodes wake up. All nodes except the source node are in state I initially. A node in state I listens at each
# round, and when receiving message Mv from transmitter v in the first c * c slots, it wakes up, and
# changes its state to S if it is in the same cell with v, or changes to A otherwise.

# A node in state A means that the node has already received the source message and will try to help
# deliver the message. Node u in state A and color j has two operations within a round. It first listens in the
# first c * c slots and then transmits message Mu with constant probability p or listens otherwise in slot c * c + j.	
# If u receives a messageMv from node v in the same cell, u changes its state to S. At the end of each round, if u
# has received the source message in the first c * c slots for k * (logn + logR) rounds, where k is a sufficiently
# large constant, u changes its state to B.

# A node in state B means that the node becomes a source message transmitter who helps to deliver the
# message. Node u in state B and color j transmits the message Mu in the jth slot of each round.

# A node in state S means that the node does not need to deliver the source message since some other nodes
# in the same cell will do that. Nodes in S do nothing in the subsequent rounds.

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import time
import copy

# Parameters 
# input
# D = {150, 200, 250, 300}
D = 150
n = 1000
R = 30
alpha = 3
beta = 1.5
P_min = R ** alpha * beta
P_max = 4 * R ** alpha * beta
epsilon = 1.0
N = P_min / ((1 + epsilon) ** alpha * R ** alpha * beta)
p = 0.2
c = 10
# zeta = {0, 1, 3, 5, 7, 9} * 10 ** (-1)
# T_zeta = {0, 1, 2, 3, 4, 5} * 10

# calc
cell_size = epsilon * R / (2 * np.sqrt(2))

c_cal = np.ceil(
    (
        ((P_max / P_min) * 
         (32 * (alpha - 1) / (alpha - 2) + 4) / 
         ((1 + epsilon / 2) ** (-alpha) - (1 + epsilon) ** (-alpha))
         ) ** (1 / alpha)
    ) * (np.sqrt(2) / epsilon) + 1
)

print(f"cell_size: {cell_size}, c_cal: {c_cal}")

# 设置随机种子以便结果可复现
# random.seed(time.time())
# 设置固定的随机种子
random.seed(42)  # 对于 Python 的 random 模块
np.random.seed(42)  # 对于 numpy 的随机函数

# 3. 初始化节点
class Node:
    def __init__(self, id, x, y, state, msg=None):
        self.id = id
        self.x = x
        self.y = y
        self.cell_id = (x // cell_size, y // cell_size)
        self.state = state
        self.message = msg
        self.inbox = []
        self.color = c * (self.cell_id[0] % c) + (self.cell_id[1] % c)
        self.cnt = 0
        self.recv = False
    
    # 节点每个时间单位的处理，定义返回值为state，表示节点的状态
    def node_process(self, slot):
        # print(f"Node {self.id} with state {self.state}")
        pstate = self.state
        if self.state == 'I':
            # if receive M_v in the first c * c slots
            if slot < c * c and self.inbox:
                msg = self.inbox.pop()
                self.inbox.clear()
                # 如果两者的cell相同
                if msg.cell_id == self.cell_id:
                    self.state = 'S'
                else:
                    self.message = Message(msg.content, self.id, self.cell_id)
                    self.state = 'A'

                print(f"Node {self.id} received message from cell {msg.cell_id} recv {len(self.inbox)}, {pstate} turn to {self.state}")

        elif self.state == 'S':
            # do nothing
            pass
        elif self.state == 'A':
            if slot < c * c and self.inbox:
                    msg = self.inbox.pop()
                    self.inbox.clear()
                    if msg.cell_id == self.cell_id:
                        self.cnt = 0
                        self.state = 'S'
                    else:
                        self.recv = True
                
            if slot == c * c + self.color:
                if random.random() < p:
                    self.broadcast()
                else:
                    if self.inbox:
                        msg = self.inbox.pop()
                        self.inbox.clear()
                        if msg.cell_id == self.cell_id:
                            self.cnt = 0
                            self.state = 'S'

            # v from node v in the same cell, u changes its state to S. At the end of each round, if u has received the source message in the first c * c slots for k * (log(n) + log(R)) rounds, where k is a sufficiently large constant, u changes its state to B.
            if slot == 2 * c * c - 1:
                self.cnt += 1
                if self.cnt >= 5 * (np.log(n) + np.log(R)):
                    self.cnt = 0
                    self.recv = False
                    self.state = 'B'
        
        elif self.state == 'B':
            if slot == self.color:
                self.broadcast()

        return self.state

    def broadcast(self):
        print(f"Node {self.id} broadcast message")
        for i in range(n):
            if self.id != i and simu.distance[self.id][i] < R:
                simu.nodes[i].inbox.append(self.message)

class Message:
    def __init__(self, content, id, cell_id):
        self.content = content + "->" + str(id)
        self.cell_id = cell_id

class Simu:
    def __init__(self, ax):
        self.ax = ax
        self.slot = 0
        self.round = 0
        self.nodes = [Node(i, random.uniform(0, D), random.uniform(0, D), 'I') for i in range(0, n)]
        # 设定第一个节点为广播节点，位置为(0, 0)
        self.nodes[0].state = 'B'
        self.nodes[0].message = Message('0', 0, self.nodes[0].cell_id)
        self.init_distance()

        # 以key:state, value: nodes的形式存储节点
        # nodes的存储方式以set的形式存储，方便节点的增删
        self.state_nodes = {'I': set(), 'A': set(), 'B': set(), 'S': set()}
        self.new_nodes = {'I': set(), 'A': set(), 'B': set(), 'S': set()}
        for node in self.nodes:
            self.state_nodes[node.state].add(node.id)

        self.annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
    
    def init_nodes(self):
        x0, y0 = random.uniform(0, D), random.uniform(0, D)
        c0 = (x0 // cell_size, y0 // cell_size)
        self.nodes.append(Node(0, x0, y0, 'B', Message('0', 0, c0)))
        for i in range(1, n):
            self.nodes.append(Node(i, random.uniform(0, D), random.uniform(0, D), 'I'))
    
    def init_distance(self):
        self.distance = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                self.distance[i][j] = np.sqrt((self.nodes[i].x - self.nodes[j].x) ** 2 + (self.nodes[i].y - self.nodes[j].y) ** 2)

    def update_annot(self, node):
        self.annot.xy = (node.x, node.y)
        text = f"ID: {node.id}\nCell ID: {node.cell_id}\nState: {node.state}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)
        self.annot.set_visible(True)  # 确保每次都设置为可见
        self.ax.figure.canvas.draw_idle()  # 立即重新绘制图形
        print(f"Node {node.id} at ({node.x:.2f}, {node.y:.2f}) cell {node.cell_id} color {node.color} state {node.state}")

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

    # 可视化
    # 处于不同状态的节点使用不同的颜色表示
    def visualize(self):
        self.ax.clear()
        self.ax.set_xlim(0, D)
        self.ax.set_ylim(0, D)
        colors = {'I': 'red', 'A': 'blue', 'B': 'green', 'S': 'orange'}
        for node in self.nodes:
            self.ax.scatter(node.x, node.y, color=colors[node.state])
        plt.draw()

    def process_node(self, node_id):
        """处理单个节点状态转换并更新状态字典"""
        state = self.nodes[node_id].node_process(self.slot)
        self.new_nodes[state].add(node_id)

    # 运行模拟
    # 每次点击模拟一个slot，每个round有2 * c * c个slot
    # def run(self):
    #     # 每次点击模拟一个slot
    #     for state in ['B', 'A', 'I', 'S']:  # 这里假设只有这三种状态需要处理
    #         for node_id in list(self.state_nodes[state]):  # 转换为列表以防在迭代时修改集合
    #             self.process_node(node_id)

    #     self.state_nodes = copy.deepcopy(self.new_nodes)
    #     self.new_nodes = {'I': set(), 'A': set(), 'B': set(), 'S': set()}
    #     self.slot += 1
    #     self.round += self.slot // (2 * c * c)
    #     self.slot %= (2 * c * c)

    #     # 打印每个状态的节点数量
    #     for state in ['I', 'A', 'B', 'S']:
    #         print(f"State {state}: {len(self.state_nodes[state])}")

    #     self.visualize()
    #     print(f"slot {self.slot} round {self.round}")

    # 每次点击模拟一个round，每个round有2 * c * c个slot
    def run(self):
        # 每次点击模拟一个round
        for _ in range(2 * c * c):
            # 每次点击模拟一个slot
            for state in ['B', 'A', 'I', 'S']:  # 这里假设只有这三种状态需要处理
                for node_id in list(self.state_nodes[state]):  # 转换为列表以防在迭代时修改集合
                    self.process_node(node_id)

            self.state_nodes = copy.deepcopy(self.new_nodes)
            self.new_nodes = {'I': set(), 'A': set(), 'B': set(), 'S': set()}
            self.slot += 1
            self.round += self.slot // (2 * c * c)
            self.slot %= (2 * c * c)

        # 打印每个状态的节点数量
        for state in ['I', 'A', 'B', 'S']:
            print(f"State {state}: {len(self.state_nodes[state])}")

        self.visualize()
        print(f"slot {self.slot} round {self.round}")

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