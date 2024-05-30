# Prim 算法的简单实现

import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import time
import prim

# Parameters 
# input
# D = {500, 1000, 2000, 3000, 4000}
# n = {16, 64, 256, 1024}
D = 4000
n = 1024
R = 800
H_MAC = 28
Payload = 84
CW_min = 31
R_D = 54000000
T_p = 3 * 10 ** (-3)
T_slot = 9 * 10 ** (-6)
T_P = 144 * 10 ** (-6)
T_PHY = 48 * 10 ** (-6)
T_difs = 28 * 10 ** (-6)

# alpha = 0.3
# alpha = 0 表示原始prim算法
alpha = 0

T_backoff = 31 * T_slot / 2
T_D = T_P + T_PHY + 8 * (H_MAC + Payload) / R_D

# 设置随机种子以便结果可复现
random.seed(time.time())
# 设置固定的随机种子
# random.seed(42)  # 对于 Python 的 random 模块
# np.random.seed(42)  # 对于 numpy 的随机函数

class NetHeader:
    def __init__(self, id, relay_num, relay_list, ttl):
        self.id = id
        self.relay_num = relay_num
        self.relay_list = relay_list
        self.ttl = ttl

class Stats:
    def __init__(self):
        self.N_f = 0
        self.amr = 0
        self.srb = 0
        self.rdn = 0
        self.T_d = 0
    
    def update(self):
        self.srb = (n - self.N_f) / n
        self.rdn = self.N_f / n
        # amr是所有node的msg_num的平均值
        self.amr = sum([node.msg_num for node in simu.nodes]) / n
        self.T_d = (simu.slot - 1) * T_p + simu.slot * (T_difs + T_backoff + T_D)

# 3. 初始化节点
class Node:
    def __init__(self, id, x, y, state, msg=None):
        self.id = id
        self.x = x
        self.y = y
        self.state = state
        self.msg_num = 0
        self.message = msg
        self.inbox = []
        self.nbrs = set()

    # 节点每个时间单位的处理，定义返回值为state，表示节点的状态
    def node_process(self):
        # print(f"Node {self.id} with state {self.state}")
        # print(f"Node {self.id} at ({self.x:.2f}, {self.y:.2f}) with state {self.state}, inbox {len(self.inbox)}")
        self.msg_num += len(self.inbox)
        if self.state == 'I':
            msg = self.inbox[-1] if self.inbox else None
            if msg:
                print(f"Node {self.id} received message from {msg.id}")
                # 遍历msg的relay_list，如果节点id在其中，则广播；否则不做任何操作
                if self.id in msg.relay_list:
                    self.state = 'B'
                    # 从msg中除去自己
                    msg.relay_list.remove(self.id)
                    msg.id = self.id
                    self.message = msg
                else:
                    self.state = 'S'
                print(f"Node {self.id} received message from {msg.id}")
        elif self.state == 'S':
            # do nothing
            pass
        elif self.state == 'B':
            do_relay = self.evaluate_relay()
            print(f"Node {self.id} do_relay: {do_relay}")
            if do_relay or self.id == 0:
                simu.stats.N_f += 1
                self.broadcast()
            # self.state = 'S'
        self.inbox = []

        return self.state

    def broadcast(self):
        print(f"Node {self.id} broadcast message")
        for i in range(n):
            if self.id != i and simu.distance[self.id][i] < R:
                simu.nodes[i].inbox.append(self.message)

    def evaluate_relay(self):
        not_reached = self.nbrs.copy()
        # emitters = {msg.id for msg in self.rcv_messages}
        # 将所有的msg.emitters合并到一个集合中
        # emitters = set()
        # for msg in self.inbox:
        #     emitters.update(msg.id)

        # for emitter in emitters:
        emitter = self.message.id
        for nbr in list(not_reached):
            if simu.distance[nbr][emitter] < R:
                not_reached.remove(nbr)

        return len(not_reached) >= alpha * len(self.nbrs)
        
class Message:
    def __init__(self, content, id, relay_num, relay_list, ttl):
        self.id = id
        self.relay_num = relay_num
        self.relay_list = relay_list
        self.ttl = ttl
        self.content = content + "->" + str(id)

class Simu:
    def __init__(self, ax, stats):
        self.ax = ax
        self.slot = 0
        self.stats = stats
        self.nodes = [Node(i, random.uniform(0, D), random.uniform(0, D), 'I') for i in range(0, n)]
        # 设定第一个节点为广播节点，位置为(0, 0)
        self.nodes[0].x, self.nodes[0].y = D / 2, D / 2
        self.nodes[0].state = 'B'
        self.w = np.random.rand(n, n) # 生成n*n的随机矩阵作为权重
        self.matrix = np.zeros((n, n))
        self.init_distance()

        prim_instance = prim.Prim()

        lists = prim_instance.prim_with_depth(self.w, 0, 7)

        relay_num = 0
        relay_list = []
        # 遍历lists
        for i, l in enumerate(lists):
            for j in l:
                if j != 0:
                    relay_num += 1
                    relay_list.append(j)
        
        print(f"relay_num: {relay_num}, relay_list: {relay_list}")

        self.nodes[0].message = Message("", 0, relay_num, relay_list, 6)

        # calc nbrs of node
        for i in range(n):
            for j in range(n):
                if i != j and self.distance[i][j] < R:
                    self.nodes[i].nbrs.add(j)

        # 以key:state, value: nodes的形式存储节点
        # nodes的存储方式以set的形式存储，方便节点的增删
        self.state_nodes = {'I': set(), 'B': set(), 'S': set()}
        self.new_nodes = {'I': set(), 'B': set(), 'S': set()}
        for node in self.nodes:
            self.state_nodes[node.state].add(node.id)

        self.annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                                 bbox=dict(boxstyle="round", fc="w"),
                                 arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.active = True  # 新添加的属性
    
    def init_nodes(self):
        x0, y0 = random.uniform(0, D), random.uniform(0, D)
        self.nodes.append(Node(0, x0, y0, 'B', Message('0', 0)))
        for i in range(1, n):
            self.nodes.append(Node(i, random.uniform(0, D), random.uniform(0, D), 'I'))
    
    def init_distance(self):
        self.distance = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                self.distance[i][j] = np.sqrt((self.nodes[i].x - self.nodes[j].x) ** 2 + (self.nodes[i].y - self.nodes[j].y) ** 2)
                if i != j and self.distance[i][j] < R:
                    self.matrix[i][j] = self.w[i][j]

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

    # 可视化
    # 处于不同状态的节点使用不同的颜色表示
    def visualize(self):
        self.ax.clear()
        self.ax.set_xlim(0, D)
        self.ax.set_ylim(0, D)
        colors = {'I': 'red', 'B': 'green', 'S': 'orange'}
        for node in self.nodes:
            self.ax.scatter(node.x, node.y, color=colors[node.state])
        plt.draw()

    def process_node(self, node_id):
        """处理单个节点状态转换并更新状态字典"""
        state = self.nodes[node_id].node_process()
        self.new_nodes[state].add(node_id)

    def print_statistics(self):
        self.stats.update()
        # print(f'slot {simu.slot}, T_p: {T_p}, T_difs: {T_difs}, T_backoff: {T_backoff}, T_D: {T_D}')
        # print(f'D: {D}, n: {n}, N_f: {self.stats.N_f}, AMR: {self.stats.amr:.2f}, SRB: {self.stats.srb:.2f}, RDN: {self.stats.rdn:.2f}, ABD: {self.stats.T_d:.4f}')
        # 假设 self.stats 是一个具有相关属性的对象
        print(
            f'D: {D:<4} n: {n:<5} N_f: {self.stats.N_f:<4} '
            f'AMR: {self.stats.amr:<6.2f} SRB: {self.stats.srb:<5.2f} '
            f'RDN: {self.stats.rdn:<5.2f} ABD: {self.stats.T_d:<7.4f}'
        )

    # 运行模拟
    # 每次点击模拟一个round，每个round有2 * c * c个slot
    def run(self):
        if not self.active:
            return
        
        # 每次点击模拟一个round
        for state in ['B', 'I', 'S']:  # 这里假设只有这三种状态需要处理
            for node_id in list(self.state_nodes[state]):  # 转换为列表以防在迭代时修改集合
                self.process_node(node_id)

        self.state_nodes = copy.deepcopy(self.new_nodes)
        self.new_nodes = {'I': set(), 'B': set(), 'S': set()}
        self.slot += 1

        # 打印每个状态的节点数量
        for state in ['I', 'B', 'S']:
            print(f"State {state}: {len(self.state_nodes[state])}")

        self.visualize()
        print(f"slot {self.slot}")
        if len(self.state_nodes['S']) == n:
            print(f"slot {self.slot} all nodes received message")
            self.ax.set_title(f"slot {self.slot} all nodes received message")
            self.print_statistics()
            self.active = False

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, D)
ax.set_ylim(0, D)
statistics = Stats()
simu = Simu(ax, statistics)
simu.visualize()

def on_click(event):
    simu.run()

fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect("motion_notify_event", simu.hover)

plt.show()