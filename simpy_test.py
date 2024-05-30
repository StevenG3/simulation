import simpy
import random

# Parameters
NETWORK_SIZE = 10  # Number of nodes in the network
TRANSMISSION_RANGE = 3  # Maximum distance for successful message transmission
JAMMING_PROBABILITY = 0.3  # Probability of a message transmission being jammed at any given time

class CentralManager:
    def __init__(self, env, nodes):
        self.env = env
        self.nodes = nodes
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(1)  # Central manager acts every simulation step
            if random.random() > JAMMING_PROBABILITY:
                # Randomly select a node to send a message if not jammed
                sender = random.choice(self.nodes)
                receiver = random.choice(self.nodes)
                if sender != receiver:
                    sender.is_transmitting = True
                    print(f"Time {self.env.now}: Node {sender.node_id} is sending a message to Node {receiver.node_id}")
                    receiver.receive_message(f"Message from Node {sender.node_id}")
                    sender.is_transmitting = False
            else:
                print(f"Time {self.env.now}: Transmission jammed")

# Node definition
class Node:
    def __init__(self, env, node_id, transmission_range):
        self.env = env
        self.node_id = node_id
        self.transmission_range = transmission_range
        self.received_messages = []
        self.action = env.process(self.behavior())

    def behavior(self):
        while True:
            # Simple simulation: periodically attempt to send a message to a random node
            target_node = random.randint(0, NETWORK_SIZE-1)
            yield self.env.timeout(1)
            if random.random() > JAMMING_PROBABILITY:
                print(f"Time {self.env.now}: Node {self.node_id} successfully sent a message to node {target_node}")
            else:
                print(f"Time {self.env.now}: Node {self.node_id}'s message to node {target_node} failed (jammed)")

# Create SimPy environment and nodes
env = simpy.Environment()

nodes = [Node(env, i, TRANSMISSION_RANGE) for i in range(NETWORK_SIZE)]
central_manager = CentralManager(env, nodes)

# Run simulation
SIMULATION_TIME = 20
env.run(until=SIMULATION_TIME)
