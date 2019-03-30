import numpy as np

class Markov:

    def __init__(self, transition_probability):
        self.transition_probability = transition_probability

    def __call__(self, possible_states: list, probability_mass_function = None, **kwargs):
        if probability_mass_function is None:
            probability_mass_function = np.ones(len(possible_states))
        rand = np.random.uniform(low = 0, high = 1)
        if rand > self.transition_probability or len(possible_states) == 0:
            return kwargs['current_state']
        else:
            return self._probability_mass_function(possible_states, probability_mass_function, **kwargs)

    def _probability_mass_function(self, states: list, probabilities: np.ndarray, **kwargs):
        probabilities /= np.sum(probabilities)
        rand = np.random.uniform(low = 0, high = 1)
        for i in range(len(states)):
            if rand < probabilities[i]:
                return states[i]
            else:
                rand -= probabilities[i]