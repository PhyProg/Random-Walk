import sys

sys.path.insert(0, "../../env")

from graph import Graph

import numpy as np

class Chain(Graph):

    def __init__(self):
        super.__init__()

    def add_node_population(self, node_id: str, population: float):
        self.nodes[node_id].add_arguments(population = population)

    def add_transition_probability(self, first: str, second: str, rate, two_way = False):
        self.nodes[first].transition_probabilities[second] = rate
        if two_way:
            self.nodes[second].transition_probabilities[first] = rate

    def get_node_transition_probability(self, node_id):
        ret = 0
        if node_id in self.node_ids:
            ret = sum(self.nodes[node_id].transition_probabilities)
        return ret

    def get_transition_matrix(self):
        no_of_nodes = len(self.node_ids)
        transition_matrix = np.zeros((no_of_nodes, no_of_nodes), dtype = np.float64)
        for node_id in self.node_ids:
            i = self.node_ids.index(node_id)
            for next_node in self.nodes[node_id].next_ids:
                j = self.node_ids.index(next_node)
                transition_matrix[i][j] = self.nodes[node_id].transition_probabilities[next_node]
        return transition_matrix