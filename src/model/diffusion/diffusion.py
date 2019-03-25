from walker import Walker

import numpy as np

class Diffusion:

    def __init__(self, grid_size: tuple, no_of_particles: (int, np.int64)):
        self.grid_size = grid_size
        self.bounds = []
        for g in self.grid_size:
            self.bounds.append((0,g))

        self.grid_dim = len(grid_size)
        self.no_of_particles = no_of_particles
        self.start_coordinates = np.zeros((self.no_of_particles, self.grid_dim), dtype = np.int32)
        self.walkers_run_data = 0

    def initialize_coordinates(self, axis, coordinates: (list, np.ndarray)):
        coordinates = np.array(coordinates)
        if axis > self.grid_dim or \
            axis < 0 or \
            coordinates.shape[0] != self.no_of_particles or \
            coordinates.shape[1] != self.grid_dim:
            raise ValueError

        for i in range(self.no_of_particles):
            self.start_coordinates[i][axis] = coordinates[i]

    def run(self, no_of_steps):
        self.walkers_run_data = np.zeros((self.no_of_particles, len(self.grid_size), no_of_steps + 1))
        for i in range(self.no_of_particles):

            wlk = Walker(no_of_steps = no_of_steps, \
                        dim = self.grid_dim, \
                        bounds = self.bounds, \
                        start_position = self.start_coordinates[i])

            wlk.walk(no_of_steps = no_of_steps)
            self.walkers_run_data[i] = wlk.get_evolution()

    def density(self, time: int, cell_size = None):
        """if cell_size is None:
            cell_size = np.ones(self.grid_dim)
        elif cell_size is list:
            if len(cell_size) == self.grid_dim:
                cell_size = np.array(cell_size)
            else:
                cell_size = np.ones(self.grid_dim)
        elif type(cell_size) is np.ndarray:
            if cell_size.shape[0] != self.grid_dim:
                cell_size = np.ones(self.grid_dim)"""

        grid = [np.linspace(0, self.grid_size[i], self.grid_size[i], dtype = np.int) for i in range(self.grid_dim)]

        bounds = [(0, self.grid_size[i]) for i in range(self.grid_dim)]

        for i in range(np.prod([grid[j].shape[0] for j in range(self.grid_dim)])):
            curr = [el(grid, i, j) for j in range(self.grid_dim)]
            temp_coords = np.array([grid[j][curr[j]] for j in range(self.grid_dim)])
            for ar in around_dd(temp_coords, bounds):
                print(curr, ar)
                

def around_dd(coord, bounds, dr = None):
    dim = coord.shape[0]
    if dr is None:
        dr = np.ones(dim)
    ret = []
    sign = [-1, 1]
    for i in range(dim):
        for sgn in sign:
            ddr = np.zeros(dim)
            ddr[i] = sgn * dr[i]
            temp = coord + ddr 
            if temp[i] >= bounds[i][0] and temp[i] <= bounds[i][1]:
                yield temp
    return ret

def el(coords, pos, until):
    it = 0
    while it < until:
        pos, _ = divmod(pos, coords[it].shape[0])
        it += 1
    _, pos = divmod(pos, coords[until].shape[0])
    return pos





if __name__ == "__main__":

    dif = Diffusion(grid_size=(100, 100), no_of_particles=100)

    dif.run(no_of_steps=5)

    print(dif.density(time=0))

