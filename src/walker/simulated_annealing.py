import numpy as np

class SimulatedAnnealing:

    def __init__(self, initial_temperature, temperature_decay = 0.9):
        self.temperature = initial_temperature
        self.tempereture_decay = temperature_decay

    def update_temprature(self):
        self.temperature *= self.tempereture_decay

    def __call__(self, possible_states: list, energies: np.ndarray, current_energy: float):
        delta_e = energies - current_energy
        probability_factors = np.exp(delta_e / self.temperature)
        probability_factors /= np.sum(probability_factors)
        rand = np.random.uniform(low = 0.0, high = 1.0)
        self.update_temprature()
        for i in range(probability_factors.shape[0]):
            if rand < probability_factors[i]:
                return possible_states[i]
            else:
                rand -= probability_factors[i]

class ThermodynamicSimulatedAnnealing(SimulatedAnnealing):
    
    def __init__(self, initial_temperature):
        self.entropy_changes = []
        self.energy_changes = []
        super().__init__(initial_temperature)

    def update_thermodynamic_parameters(self, delta_energy):
        #TODO
        return

    def __call__(self, possible_states: list, energies: np.ndarray, current_energy: float):
        delta_e = energies - current_energy
        probability_factors = np.exp(delta_e / self.temperature)
        probability_factors /= np.sum(probability_factors)
        rand = np.random.uniform(low = 0.0, high = 1.0)
        for i in range(probability_factors.shape[0]):
            if rand < probability_factors[i]:
                self.update_thermodynamic_parameters(delta_e[i])
                return possible_states[i]
            else:
                rand -= probability_factors[i]