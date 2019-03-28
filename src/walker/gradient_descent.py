import numpy as np

class GradientDescent:

    def __init__(self):
        return

    def __call__(self, possible_states: list, energies: np.ndarray):
        return possible_states[np.argmin(energies)]
    