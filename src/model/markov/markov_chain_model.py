import sys

sys.path.insert(0, "../../env")
sys.path.insert(0, "../../walker")

from chain import Chain
from node import Node

from markov import Markov
from light_walker import LightWalker

import numpy as np


class MarkovChainModel:

    def __init__(self, **kwargs):
        self.chain = Chain()
        self.walkers = []
        
        self.dt = 1e-7
        self.update_time_unit_(**kwargs)

        self.error = 1e-7
        self.update_error_(**kwargs)

    def update_time_unit_(self, **kwargs):
        if 'dt' in kwargs.keys():
            try:
                self.dt = np.float64(kwargs['dt'])
                del kwargs['dt']
            except: ValueError

    def update_error_(self, **kwargs):
        if 'error' in kwargs.keys():
            try:
                self.error = np.float64(kwargs['error'])
                del kwargs['error']
            except: ValueError 

    def add_nodes_(self, nodes_population, **kwargs):
        nodes_population = np.array(nodes_population)

        for i in range(nodes_population.shape[0]):
            node = Node(population = nodes_population[i])
            self.chain.add_nodes(node)

        if 'transition_matrix' in kwargs.keys():
            transition_matrix = kwargs['transition_matrix']
        else:
            transition_matrix = np.zeros((self.chain.no_of_nodes, self.chain.no_of_nodes), dtype = np.float65)

        self.add_transition_probabilities_to_nodes_(transition_matrix)
        self.initialize_walkers_(nodes_population)

    def add_transition_probabilities_to_nodes_(self, transition_matrix):
        for i in range(transition_matrix.shape[0]):
            self.chain.nodes[self.chain.node_ids[i]].add_arguments(\
                transition_probabilities = {})
            for j in range(transition_matrix.shape[1]):
                if transition_matrix[i][j] > self.error:
                    self.chain.add_transition_probability(self.chain.node_ids[i], \
                                                        self.chain.node_ids[j],
                                                        transition_matrix[i][j])

    def initialize_walkers_(self, population):
        return
