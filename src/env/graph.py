from node import Node
from copy import deepcopy
from random import choice

import string

class Graph:

    nodes = {}
    node_ids = []

    def __init__(self):
        self.nodes = {}
        self.node_ids = []
        return

    def add_node(self, node: Node):
        id = self.get_id()
        self.node_ids.append(id)
        self.nodes[id] = deepcopy(node)
        self.nodes[id].node_id = id

    def remove_node(self, node_id: str):
        if node_id in self.node_ids:
            for prev_id in self.nodes[node_id].prev_ids:
                self.nodes[prev_id].remove_next_id(node_id)
            for next_id in self.nodes[node_id].next_ids:
                self.nodes[next_id].remove_prev_id(node_id)

    def add_connection(self, first: str, second:str, one_way = True):
        if first not in self.node_ids or second not in self.node_ids:
            return
        if second not in self.nodes[first].next_ids:
            self.nodes[first].next_ids.append(second) 
        if first not in self.nodes[second].prev_ids:
            self.nodes[second].prev_ids.append(first)
        if not one_way:
            if second not in self.nodes[first].prev_ids:
                self.nodes[first].prev_ids.append(second) 
            if first not in self.nodes[second].next_ids:
                self.nodes[second].next_ids.append(first)

    def get_id(self, size = 30):
        id = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(size))
        while id in self.node_ids:
            id = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return id

    def __str__(self):
        return

    def graph_data(self):
        temp = "Number of nodes: " + str(len(self.node_ids))
        yield temp 
        temp = "Node Ids:" 
        yield temp 
        for node_id in self.node_ids:
            temp = "\t" + node_id
            yield temp

    def print_data(self, stream, default_startswith = ""):
        stream.write(default_startswith + "Graph:" + "\n")
        for data in self.graph_data():
            stream.write(default_startswith + "\t" + data + "\n")
        self.print_node_data(stream, default_startswith = "\t")

    def print_node_data(self, stream, default_startswith = ""):
        for node in self.nodes.values():
            node.print_data(stream, default_startswith = default_startswith) 