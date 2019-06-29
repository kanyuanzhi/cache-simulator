import random

class Node(object):
    def __init__(self, size, network, type, pattern, node_id=-1):
        # type options: leaf, router, root
        self.size = size
        # self.amount = amount
        # self.staleness = staleness # expected value
        self.type = type
        self.pattern = pattern

        self.id = node_id

        self.next_node = None
        # self.previous_nodes = []

        self.network = network

        self.stack = []
        self.hit = 0
        self.miss = 0

        self.updatetime_in_cache = {}
        self.validation_time_in_cache = {}

        
    def nextNode(self, node):
        self.next_node = node

    # def previousNode(self, node):
    #     self.previous_node = node

    def insert(self, item, now):
        if self.pattern == "reactive":
            if item in self.stack:
                if now - self.updatetime_in_cache[item] < self.validation_time_in_cache[item]:
                    self.hit = self.hit + 1
                    self.network.hitCount()
                else:
                    self.updatetime_in_cache[item] = self.network.updatetime[item]
                    self.validation_time_in_cache[item] = self.network.validation_time[item]
                    self.miss = self.miss + 1
                    self.next_node.insert(item, now)
                self.stack.remove(item)
                self.stack.append(item)
            else:
                self.miss = self.miss + 1
                self.save(item)
                self.updatetime_in_cache[item] = self.network.updatetime[item]
                self.validation_time_in_cache[item] = self.network.validation_time[item]
                if self.type == "root":
                    self.network.missCount()
                else:
                    self.next_node.insert(item, now)
        else:
            if item in self.stack:
                self.hit = self.hit + 1
                self.network.hitCount()
                self.stack.remove(item)
                self.stack.append(item)
            else: 
                self.miss = self.miss + 1
                self.save(item)
                if self.type == "root":
                    self.network.missCount()
                else:
                    self.next_node.insert(item, now)
            # if self.type == "root":
            #     self.save(node_id, item)
            #     for node in self.previous_nodes:
            #         if node.id == node_id:
            #             self.node.save(node_id, item)
            # else:
            #     self.next_node.forward(self.id, item, now)
    
    def save(self, item):
        if len(self.stack) == self.size:
            self.stack.pop(0)
            self.stack.append(item)
        else:
            self.stack.append(item)

    