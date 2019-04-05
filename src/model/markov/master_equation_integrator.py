import numpy as np
from scipy.integrate import solve_ivp

class MasterEquationIntegrator:

    def __init__(self):
        pass
    
    def get_fun(self, transition_matrix, populations):
        transition_matrix = np.array(transition_matrix)
        populations = np.array(populations)

        ret = np.zeros(populations.shape[0])

        for i in range(populations.shape[0]):
            for j in range(populations.shape[0]):
                if i == j:
                    continue
                ret[i] += transition_matrix[j][i] * populations[j]
                ret[i] -= transition_matrix[i][j] * populations[i]
        
        return ret

    def __call__(self, transition_matrix, populations, time_span, t_eval = None):
        fun = lambda t, y: self.get_fun(transition_matrix, y)
        sol = solve_ivp(fun, time_span, populations, t_eval = t_eval)
        return sol.t, sol.y

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    populations = np.array([10, 20, 35, 45, 50])

    transition_matrix = [[0, 0, 0, 0, 0],\
                         [1, 0, 1, 1, 1],\
                         [1, 1, 0, 1, 0],\
                         [1, 0, 0, 0, 1],\
                         [1, 1, 1, 1, 0]]

    transition_matrix = np.array(transition_matrix, dtype = np.float) * 5

    integrator = MasterEquationIntegrator()

    sol_t, sol_y = integrator(transition_matrix, populations, time_span = (0, 1.), t_eval = np.arange(0, 1, 1e-5))

    for yy in sol_y:
        plt.plot(sol_t, yy)
    plt.show()

    print(sol_t)