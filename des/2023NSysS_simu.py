import simpy
import random

# Constants
TIMER_SLOT = 1  # 1 ms as specified, can be adjusted based on simulation setup

class Station:
    def __init__(self, env, id, neighbors):
        self.env = env
        self.id = id
        self.neighbors = set(neighbors)
        self.received_messages = set()
        self.action = env.process(self.run())

    def run(self):
        while True:
            message = yield self.env.timeout(TIMER_SLOT)  # Wait for a message
            if message:
                self.process_message(message)

    def process_message(self, message):
        if message.id not in self.received_messages:
            self.received_messages.add(message.id)
            # Check if need to rebroadcast
            if self.should_rebroadcast(message):
                self.schedule_rebroadcast(message)

    def should_rebroadcast(self, message):
        # Determine if there are any uncovered neighbors
        uncovered_neighbors = self.neighbors - message.covered
        return bool(uncovered_neighbors)

    def schedule_rebroadcast(self, message):
        deg = len(self.neighbors)
        deg_max = max([len(n.neighbors) for n in self.neighbors])
        t_0 = 1 / deg + 1 / deg_max
        t = TIMER_SLOT * random.uniform(0, t_0)  # Adjust the randomness as needed
        yield self.env.timeout(t)
        self.env.process(self.rebroadcast(message))

    def rebroadcast(self, message):
        # Add your logic to rebroadcast the message to neighbors
        print(f'Station {self.id} rebroadcasting message at time {self.env.now}')
        for neighbor in self.neighbors:
            neighbor.process_message(message)

class Message:
    def __init__(self, id, source, covered):
        self.id = id
        self.source = source
        self.covered = covered

def setup(env, num_stations):
    stations = [Station(env, i, set()) for i in range(num_stations)]
    # Setup neighbors (example setup, should be derived from your network topology)
    for i in range(num_stations):
        if i < num_stations - 1:
            stations[i].neighbors.add(stations[i + 1])
            stations[i + 1].neighbors.add(stations[i])

    # Start a broadcast from a source station
    source_station = stations[0]
    initial_message = Message(id=1, source=source_station, covered=set())
    env.process(source_station.rebroadcast(initial_message))

env = simpy.Environment()
setup(env, 10)  # Setup with 10 stations
env.run(until=100)  # Run the simulation for 100 time units