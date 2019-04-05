import sys

sys.path.insert(0, "../../env")

from graph import Graph

from copy import deepcopy

import numpy as np

class Chain(Graph):

    def __init__(self):
        self.population_changes = {}
        self.time_series = 0
        super(Chain, self).__init__()
        return

    def add_node_population(self, node_id: str, population: float):
        self.nodes[node_id].add_arguments(population = population)

    def add_transition_probability(self, first: str, second: str, rate, two_way = False):
        self.add_connection(first, second, one_way = not two_way)
        self.nodes[first].transition_probabilities[second] = rate
        if two_way:
            self.nodes[second].transition_probabilities[first] = rate

    def get_node_transition_probability(self, node_id):
        ret = 0
        if node_id in self.node_ids:
            for val in self.nodes[node_id].transition_probabilities.values():
                ret += val
        return ret

    def get_node_probability_mass_function(self, node_id):
        if node_id in self.node_ids:
            return self.nodes[node_id].transition_probabilities

    def update_markov_model(self):
        for node_id in self.node_ids:
            tr = self.get_node_transition_probability(node_id)
            self.nodes[node_id].add_arguments(transition_probability = tr)

    def adjust_node_populations(self, change: dict):
        for node, change in zip(change.keys(), change.values()):
            self.nodes[node].population += change

    def update_node_populations(self, population_changes, time_series):
        self.time_series = time_series
        self.population_changes = deepcopy(population_changes)

    def get_population_time_series(self, node_id, time = -1):
        ts = self.nodes[node_id].population
        l = self.population_changes[node_id][:time].shape[0]
        ts = np.array([ts + np.sum(self.population_changes[node_id][:i]) for i in range(l)])
        return ts

    def get_transition_matrix(self):
        no_of_nodes = len(self.node_ids)
        transition_matrix = np.zeros((no_of_nodes, no_of_nodes), dtype = np.float64)
        for node_id in self.node_ids:
            i = self.node_ids.index(node_id)
            for next_node in self.nodes[node_id].next_ids:
                j = self.node_ids.index(next_node)
                transition_matrix[i][j] = self.nodes[node_id].transition_probabilities[next_node]
        return transition_matrix