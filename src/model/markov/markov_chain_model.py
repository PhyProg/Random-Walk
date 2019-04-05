import sys

sys.path.insert(0, "../../env")
sys.path.insert(0, "../../walker")

from chain import Chain
from graph import Graph
from node import Node

from markov import Markov
from walker import Walker

import numpy as np


from IPython.display import display, clear_output 


class MarkovChainModel:

    def __init__(self, **kwargs):
        self.chain = Chain()
        self.walkers = []
        
        self.times = np.zeros(1)
        self.dt = 1e-7
        self.update_time_unit_(**kwargs)

        self.error = 1e-7
        self.update_error_(**kwargs)

        pop = None
        dat = None

        try:
            pop = kwargs['node_population']
        except: KeyError

        try:
            dat = kwargs['node_data']
        except: KeyError

        self.add_nodes_(pop, dat, **kwargs)

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

    def add_nodes_(self, nodes_population, nodes_data_dict = None, **kwargs):
        nodes_population = np.array(nodes_population)

        if nodes_data_dict is None:
            nodes_data_dict = [{} for i in range(nodes_population.shape[0])]

        for i in range(nodes_population.shape[0]):
            node = Node(population = nodes_population[i], **nodes_data_dict[i])
            self.chain.add_node(node)

        if 'transition_matrix' in kwargs.keys():
            transition_matrix = kwargs['transition_matrix']
        else:
            transition_matrix = np.zeros((self.chain.no_of_nodes, self.chain.no_of_nodes),\
                                         dtype = np.float64)

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
                                                        transition_matrix[i][j] * self.dt)
        self.chain.update_markov_model()

    def initialize_walkers_(self, population):
        for i in range(self.chain.no_of_nodes):
            trans_prob = self.chain.get_node_transition_probability(self.chain.node_ids[i])
            next_step_processor = Markov(trans_prob)
            for j in range(population[i]):
                wlk = Walker(next_step_processor = next_step_processor,\
                                initial_id = self.chain.node_ids[i])
                self.walkers.append(wlk)

    def run(self, time, display_progress = True):
        self.times = np.arange(0, time + self.dt, self.dt)

        population_changes = {key: np.zeros(self.times.shape[0]) for key in self.chain.node_ids}

        iteration = 1
        
        if display_progress:
            self._display_progress(self.times[0])

        for tt in self.times[1:]:
            for walker in self.walkers:
                curr = walker.current_position()
                walker.next_step_processor.transition_probability = \
                                                        self.chain.nodes[curr].transition_probability
                next_pos = self.chain.next(curr)
                if len(next_pos) == 0:
                    walker.empty_step()
                    continue
                pmf = self.chain.get_node_probability_mass_function(curr)
                pmf = [pmf[pos] for pos in next_pos]
                walker.walk(possible_states = next_pos, \
                            current_state = curr, \
                            probability_mass_function = pmf)

                nxt = walker.current_position()

                population_changes[curr][iteration] -= 1
                population_changes[nxt][iteration] += 1

                #print(population_changes)

            iteration += 1
            if display_progress:
                self._display_progress(tt)

        self.chain.update_node_populations(population_changes, self.times)

    def get_population_time_series(self, time = -1, nodes = []):
        ret = []
        for node in nodes:
            if node in self.chain.node_ids:
                node_id = node
            elif type(node) is int:
                node_id = self.chain.node_ids[node]
            else:
                node_id = self.chain.node_ids[-1]

            ret.append(self.chain.get_population_time_series(node_id = node_id, time = time))
        return self.times[1:], ret

    def write_population_data(self, stream = None, path = None):
        data = self.get_population_time_series(nodes = self.chain.node_ids)
        data = (np.append(data[0], data[1])).reshape((len(data[1]) + 1, data[0].shape[0]))
        if type(path) is str:
            np.savetxt(path, data)
        elif stream is not None:
            stream.write(data)

    def _display_progress(self, current_progress):
        idx = np.where(self.times - current_progress >= 0)[0][0] + 1
        perc = int(100. * idx / self.times.shape[0])
        clear_output(wait = True)
        prg = "["
        prg += "".join(["=" for i in range(int(perc / 5))])
        prg += "".join(["." for i in range(20 - int(perc / 5))])
        prg += "".join("]")
        display(prg + "       " + 'Progress: ' + str(perc) + "%")
        #sys.stdout.flush(prg + "       " + 'Progress: ' + str(perc))


if __name__ == "__main__":
    model = MarkovChainModel(node_population = 10 * np.array([10, 20, 35, 45, 50]), dt = 1e-2)

    transition_matrix = [[0, 0, 0, 0, 0],\
                         [1, 0, 1, 1, 1],\
                         [1, 1, 0, 1, 0],\
                         [1, 0, 0, 0, 1],\
                         [1, 1, 1, 1, 0]]

    transition_matrix = np.array(transition_matrix, dtype = np.float) * 5

    model.add_transition_probabilities_to_nodes_(transition_matrix)
    #s = Chain()
    model.run(time = 1)

    ts, arr = model.get_population_time_series(nodes = [0, 1, 2, 3, 4])

    import matplotlib.pyplot as plt
    for ar in arr:
        plt.plot(ts, ar)
    plt.show()