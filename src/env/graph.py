from node import Node
from copy import deepcopy
from random import choice

import numpy as np

import string

class Graph:

    def __init__(self, id_generator = None):
        self.nodes = {}
        self.node_ids = []
        self.no_of_nodes = 0
        if id_generator is not None:
            self.manual_hashing = True
            self.id_generator = id_generator
        else:
            self.manual_hashing = False
        return

    def add_node(self, node: Node, coordinates = None):
        self.no_of_nodes += 1
        id = self.get_id(coordinates)       
        self.node_ids.append(id)
        self.nodes[id] = deepcopy(node)
        self.nodes[id].node_id = id

    def remove_node(self, node_id: str):
        if node_id in self.node_ids:
            self.no_of_nodes -= 1
            self.node_ids.remove(node_id)
            del self.nodes[node_id]
            for prev_id in self.nodes[node_id].prev_ids:
                self.nodes[prev_id].remove_next_id(node_id)
            for next_id in self.nodes[node_id].next_ids:
                self.nodes[next_id].remove_prev_id(node_id)

    def add_connection(self, first: str, second: str, one_way = True):
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

    def next(self, current: str):
        return self.nodes[current].next_ids

    def get_keys(self):
        return list(self.nodes.keys())

    def get_id(self, coordinates = None, size = 30):
        if self.manual_hashing and type(coordinates) is np.ndarray or coordinates is list:
            id = self.id_generator(coordinates)
        else:
            id = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(size))
            while id in self.node_ids:
                id = ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(size))
        return id

    def __str__(self):
        return

    def graph_data(self):
        temp = "Number of nodes: " + str(len(self.node_ids))
        yield temp 
        temp = "Manual hashing: " + str(self.manual_hashing)
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