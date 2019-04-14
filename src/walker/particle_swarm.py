import sys

sys.path.insert(0, "../")

from walker.light_walker import LightWalker 
from env.metric import InnerProductL2
import numpy as np

class ParticleSwarm:

    def __init__(self, \
                grid_dim, \
                no_of_walkers, \
                inner_product: callable, \
                initial_positions = None,
                data_collection_keys = [],
                max_no_of_steps = 1e5,
                social_learning_coef = 1,
                cognitive_learning_coef = 1):
        
        self.dim = grid_dim
        self.no_of_walkers = no_of_walkers
        self.initial_positions = initial_positions
        self.max_no_of_steps = 1e8
        self.walkers = []

        processor = SwarmIntelligenceProcessor(inner_product)

        for i in range(self.no_of_walkers):
            inp = 0
            try:
                inp = initial_positions[i]
            except TypeError:
                inp = None
            wlk = LightWalker(next_step_processor=processor,\
                            data_collection_keys=data_collection_keys,\
                            dim = self.dim,\
                            initial_position=inp,\
                            max_no_of_steps=max_no_of_steps)
            self.walkers.append(wlk)
        
        self.social_learning_coef = social_learning_coef
        self.cognitive_learning_coef = cognitive_learning_coef

        self.global_optimal_pos = np.zeros(self.dim)
        self.local_optimal_pos = np.zeros((self.no_of_walkers, self.dim))

        self.global_optimal_value = np.inf
        self.local_optimal_values = np.inf * np.ones(self.no_of_walkers)

        self.walker_velocities = np.random.uniform(low = 0, high = 1, \
                                                size = self.no_of_walkers * self.dim)\
                                                .reshape((self.no_of_walkers, self.dim))

    def walk(self, index_of_walker, possible_states, possible_states_energies):
        velocity = self._get_walker_velocity(index_of_walker)
        self.walkers[index_of_walker].walk(possible_states = possible_states, velocity = velocity)
        #self.update_optimal_values(index_of_walker, 31)

    def update_optimal_values(self, index_of_walker, energy_of_state):
        pos = self.walkers[index_of_walker].get_current_position()
        #print(energy_of_state, self.global_optimal_value, self.local_optimal_values[index_of_walker])
        if energy_of_state < self.global_optimal_value:
            self.local_optimal_pos[index_of_walker] = pos
            self.global_optimal_pos = pos
            self.local_optimal_values[index_of_walker] = energy_of_state
            self.global_optimal_value = energy_of_state
        elif energy_of_state < self.local_optimal_values[index_of_walker]:
            self.local_optimal_pos[index_of_walker] = pos
            self.local_optimal_values[index_of_walker] = energy_of_state

    def _get_walker_info(self, index_of_walker):
        return self.walkers[index_of_walker].get_current_position(), \
                self.walkers[index_of_walker].data_collection_keys

    def _get_walker_velocity(self, index_of_walker):
        r1, r2 = np.random.uniform(size = 2)

        self.walker_velocities[index_of_walker] += self.cognitive_learning_coef * r1 * \
            (self.local_optimal_pos[index_of_walker] - self.walkers[index_of_walker].get_current_position()) \
            + self.social_learning_coef * r2 * \
            (self.global_optimal_pos - self.walkers[index_of_walker].get_current_position())

        return self.walker_velocities[index_of_walker]


class SwarmIntelligenceProcessor:

    def __init__(self, inner_product: callable):
        self.inner_product = inner_product

    def _choose(self, pmf : np.ndarray):
        rand = np.random.uniform(low = 0., high = 1.)
        for i in range(pmf.shape[0]):
            if rand < pmf[i]:
                return i
            else:
                rand -= pmf[i]
        return pmf.shape[0] - 1


    def __call__(self, positions: list, velocity: np.ndarray):
        norm_vel = np.sqrt(self.inner_product(velocity, velocity))
        norms_ = np.sqrt(list((self.inner_product(pos, pos) for pos in positions)))

        pmf = [(self.inner_product(velocity, pos) / (norm_vel * norm_pos) + 1.) \
                for pos, norm_pos in zip(positions, norms_)]

        #print(pmf)

        pmf = np.array(pmf) / np.sum(pmf)

        #print(pmf)

        return positions[self._choose(pmf)]



if __name__ == "__main__":

    no_of_walkers = 100

    ip = InnerProductL2()

    swarm = ParticleSwarm(grid_dim = 1, no_of_walkers = 100, inner_product = ip)

    for i in range(100):
        swarm.walk(i, [np.array(1), np.array(2), np.array(3)], [3, 2, 1])

    print(swarm.__dict__)