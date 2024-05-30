
import parameters

class Node(object):
    def __init__(self, env, id, x, y, stats):
        self.env = env
        self.id = id
        self.x = x
        self.y = y
        self.stats = stats
        print('%s created with coordinates %d %d' % (self.id, self.x, self.y))

    def send(self, destination, length, id):
        if parameters.PRINT_LOGS:
            print('Time %d: Node%d sends %s to %d' % (self.env.now, self.id, id, destination))
        yield self.env.process(self.mac.send(destination, length, id))

    def receive(self, id, source):
        if parameters.PRINT_LOGS:
            print('Time %d: %s receives %s from %s' % (self.env.now, self.name, id, source))