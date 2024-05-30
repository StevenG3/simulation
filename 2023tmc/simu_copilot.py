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
D = {150, 200, 250, 300}
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
zeta = {0, 1, 3, 5, 7, 9} * 10 ** (-1)
T_zeta = {0, 1, 2, 3, 4, 5} * 10

# 3. Initialize nodes
class Node:
    def __init__(self, x, y, state, color, message):
        self.x = x
        self.y = y
        self.state = state
        self.color = color
        self.message = message

    def distance(self, node):
        return math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def receive(self, node):
        if self.state == 'I':
            if self.distance(node) <= R:
                self.state = 'S' if self.color == node.color else 'A'
        elif self.state == 'A':
            if self.color == node.color:
                self.state = 'S'
        elif self.state == 'B':
            pass
        elif self.state == 'S':
            pass

# 4. Initialize the network
nodes = []
for i in range(n):
    x = random.uniform(0, D)
    y = random.uniform(0, D)
    state = 'I'
    color = random.randint(0, c * c - 1)
    message = None
    nodes.append(Node(x, y, state, color, message))

# 5. Start the simulation
for t in range(T_zeta):
    # 6. Regular jamming
    for node in nodes:
        if random.random() < zeta:
            node.state = 'I'

    # 7. Message dissemination
    for node in nodes:
        if node.state == 'I':
            for other in nodes:
                node.receive(other)
        elif node.state == 'A':
            if random.random() < p:
                pass
        elif node.state == 'B':
            pass
        elif node.state == 'S':
            pass

# 8. Evaluate the performance
def evaluate(nodes):
    cnt = 0
    for node in nodes:
        if node.state == 'S':
            cnt += 1
    return cnt

print(evaluate(nodes))

# 9. Plot the network
def plot(nodes):
    for node in nodes:
        if node.state == 'S':
            plt.scatter(node.x, node.y, color='red')
        else:
            plt.scatter(node.x, node.y, color='blue')
    plt.show()

plot(nodes)

# 10. Save the network
def save(nodes):
    with open('nodes.txt', 'w') as f:
        for node in nodes:
            f.write(f'{node.x} {node.y} {node.state} {node.color}\n')

save(nodes)

# 11. Load the network
def load():
    nodes = []
    with open('nodes.txt', 'r') as f:
        for line in f:
            x, y, state, color = line.split()
            nodes.append(Node(float(x), float(y), state, int(color), None))
    return nodes

nodes = load()