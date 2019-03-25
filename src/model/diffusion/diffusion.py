import sys

sys.path.append("../../")

from model.diffusion.walker import Walker

import numpy as np
import math

class Diffusion:

    def __init__(self, grid_size: tuple, no_of_particles: (int, np.int64)):
        self.grid_size = grid_size
        self.bounds = []
        for g in self.grid_size:
            self.bounds.append((0,g))

        self.grid_dim = len(grid_size)
        self.no_of_particles = np.int64(no_of_particles)
        self.start_coordinates = np.zeros((self.no_of_particles, self.grid_dim), dtype = np.int32)
        self.walkers_run_data = np.zeros((self.no_of_particles, len(self.grid_size), 1))

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
        no_of_steps = np.int64(no_of_steps)
        self.walkers_run_data = np.zeros((self.no_of_particles, len(self.grid_size), no_of_steps + 1))
        
        for i in range(self.no_of_particles):

            wlk = Walker(no_of_steps = no_of_steps, \
                        dim = self.grid_dim, \
                        bounds = self.bounds, \
                        start_position = self.start_coordinates[i])

            wlk.walk(no_of_steps = no_of_steps)
            self.walkers_run_data[i] = wlk.get_evolution()

    def density(self, time: int, cell_size = None):
        if cell_size is None:
            cell_size = np.ones(self.grid_dim)
        elif cell_size is list:
            if len(cell_size) == self.grid_dim:
                cell_size = np.array(cell_size)
            else:
                cell_size = np.ones(self.grid_dim)
        elif type(cell_size) is np.ndarray:
            if cell_size.shape[0] != self.grid_dim:
                cell_size = np.ones(self.grid_dim)

        density = np.zeros((tuple(np.int(self.grid_size[i] / cell_size[i]) for i in range(self.grid_dim))), dtype = np.int) \
                #for i in range(self.grid_dim)]

        for i in range(self.no_of_particles):
            coords = self.embedd(self.walkers_run_data[i,:,time], cell_size)
            density[tuple(coords)] += 1

        return density

    def embedd(self, coordinates, cell_size):
        ret = []
        for i in range(self.grid_dim):
            _, c = math.modf(coordinates[i] / cell_size[i])
            ret.append(int(c))
        return ret

    def get_run_data(self, time):
        return self.walkers_run_data[:,:,time]

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

    dif.run(no_of_steps=10)

    dns = dif.density(10, cell_size=[3,3])

    print(dns)
    print(dns.shape)
    print(np.sum(dns))

