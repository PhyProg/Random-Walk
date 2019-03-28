import numpy as np

class Markov:

    def __init__(self, transition_probability, other: callable):
        self.other = other
        self.transition_probability = transition_probability

    def __call__(self, current_state, possible_states: list, **kwargs):
        rand = np.random.uniform(low = 0, high = 1)
        if rand > self.transition_probability:
            return current_state
        else:
            return self.other(possible_states, **kwargs)