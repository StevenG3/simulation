import matplotlib.pyplot as plt
import numpy as np
from numpy import mean, std
from scipy import misc

import flood
import pflood
import prim
import pprim
import mda

import parameters

class Stats(object):
    def __init__(self):
        self.generatedPacketsTimes = {}    # packet id - timestamp of generation
        self.deliveredPacketsTimes = {}    # packet id - timestamp of delivery

    def logGeneratedPacket(self, id, timestamp):
        self.generatedPacketsTimes[id] = timestamp

    def logDeliveredPacket(self, id, timestamp):
        self.deliveredPacketsTimes[id] = timestamp

    def printGeneratedPacketTimes(self):
        for generatedPacket in self.generatedPacketsTimes:
            print (self.generatedPacketsTimes[generatedPacket])

    def printDeliveredPacketTimes(self):
        for deliveredPacket in self.deliveredPacketsTimes:
            print (self.deliveredPacketsTimes[deliveredPacket])

    def plotForwardingNodes(self):
        plt.figure(1)

        plt.plot(parameters.NUMBER_OF_NODES, flood.forwardingNodes, 'r-o',  label='flood')
        plt.plot(parameters.NUMBER_OF_NODES, pflood.forwardingNodes, 'b-^', label='p-flood')
        plt.plot(parameters.NUMBER_OF_NODES, prim.forwardingNodes,   'g-s',  label='prim')
        plt.plot(parameters.NUMBER_OF_NODES, pprim.forwardingNodes,  'm-d', label='P-prim')
        plt.plot(parameters.NUMBER_OF_NODES, mda.forwardingNodes,    'c-p',  label='MDA')

        plt.legend()
        plt.xlabel('Number of nodes')
        plt.ylabel('Number of forwarding nodes')
        plt.legend()
        file = 'results/packets' + '.pdf'
        plt.savefig(file, bbox_inches='tight', dpi=250)
