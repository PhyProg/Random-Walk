import numpy as np

class SimulatedAnnealing:

    def __init__(self, initial_temperature, temperature_decay = 0.9):
        self.temperature = initial_temperature
        self.tempereture_decay = temperature_decay

    def update_temprature(self, delta_energy):
        if delta_energy > 0:
            self.temperature *= self.tempereture_decay

    def __call__(self, possible_states: list, energies: np.ndarray, current_energy: float):
        delta_e = energies - current_energy
        probability_factors = np.exp(delta_e / self.temperature)
        probability_factors /= np.sum(probability_factors)
        rand = np.random.uniform(low = 0.0, high = 1.0)
        for i in range(probability_factors.shape[0]):
            if rand < probability_factors[i]:
                self.update_temprature(delta_e[i])
                return possible_states[i]
            else:
                rand -= probability_factors[i]

class ThermodynamicSimulatedAnnealing(SimulatedAnnealing):
    
    def __init__(self, initial_temperature, temperature_decay):
        self.entropy_changes = 0
        self.energy_changes = 0
        super().__init__(initial_temperature, temperature_decay)

    def update_thermodynamic_parameters(self, delta_energy):
        if delta_energy < 0:
            return
        self.energy_changes += delta_energy
        self.entropy_changes += delta_energy / self.temperature
        if self.entropy_changes > 0:
            self.temperature = self.tempereture_decay * self.energy_changes / self.entropy_changes

    def __call__(self, possible_states: list, energies: np.ndarray, current_energy: float):
        delta_e = energies - current_energy
        probability_factors = np.exp(-delta_e / self.temperature)
        probability_factors /= np.sum(probability_factors)
        rand = np.random.uniform(low = 0.0, high = 1.0)
        for i in range(probability_factors.shape[0]):
            if rand < probability_factors[i]:
                self.update_thermodynamic_parameters(delta_e[i])
                return possible_states[i]
            else:
                rand -= probability_factors[i]

class QuantumAnnealing:

    def __init__(self, transition_probability):
        self.transition_probability = transition_probability
        self.transition_probability_fluctuations = 0

    def update_transition_probability(self, delta_energy):
        return

    def __call__(self, possible_states:list, current_energy, energies: np.ndarray, width: np.ndarray):
        delta_e = energies - current_energy
        probability_factors = np.exp(np.sqrt(delta_e) * width / self.transition_probability)
        probability_factors /= np.sum(probability_factors)
        rand = np.random.uniform(low = 0.0, high = 1.0)
        for i in range(probability_factors.shape[0]):
            if rand < probability_factors[i]:
                self.update_transition_probability(delta_e[i])
                return possible_states[i]
            else:
                rand -= probability_factors[i]

