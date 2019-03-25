import numpy as np 
from random import choice

class Walker:

    def __init__(self, no_of_steps = 1e8, dim = 2, bounds = None, start_position = None):
        
        self.confined = []
        self.unbounded = []
        self.bounds = []

        if bounds is None:
            self.bounds = np.array([(-np.inf, np.inf) for i in range(dim)])
            self.unbounded = [True for i in range(dim)]
            self.confined = [False for i in range(dim)]
        else:
            for bound in bounds:
                if bound is None:
                    self.bounds.append((-np.inf, np.inf))
                    self.unbounded.append(True)
                    self.confined.append(False)
                else:
                    self.bounds.append(bound)
                    self.unbounded.append(False)
                    if bound[1] == bound[0]:
                        self.confined.append(True)
                    else:
                        self.confined.append(False)
            self.bounds = np.array(self.bounds)

        no_of_steps = np.int64(no_of_steps)

        self.curr_step = 0
        self.time = np.linspace(0, no_of_steps, no_of_steps + 1, dtype = np.int64)
        self.moves = np.zeros((dim, no_of_steps), dtype = np.int)
        self.dim = dim
        self.no_of_steps = no_of_steps

        self.start_position = 0
        self.update_start_position(start_position)
    
    def update_start_position(self, start_position):
        if start_position is list:
            if len(start_position) == self.dim:
                self.start_position = np.array(start_position)
        elif type(start_position) is np.ndarray:
            if start_position.shape[0] == self.dim:
                self.start_position = start_position
        else:
            self.start_position = self.get_default_start_position()

        for ax in range(self.dim):
            if not self.unbounded[ax]:
                if self.start_position[ax] < np.int(self.bounds[ax, 0]) or \
                    self.start_position[ax] > np.int(self.bounds[ax, 1]):
                    raise ValueError

    def get_default_start_position(self):
        start_pos = []
        for ax in range(self.dim):
            if self.unbounded[ax]:
                start_pos.append(0)
            elif self.confined[ax]:
                start_pos.append(self.bounds[ax, 0])
            elif 0 >= self.bounds[ax][0] and 0 <= self.bounds[ax][1]:
                start_pos.append(0)
            else:
                start_pos.append(np.mean(self.bounds[ax]))
        return np.array(start_pos, dtype = np.int)

    def reset(self, start_position = None):
        if start_position is not None:
            self.update_start_position(start_position)
        self.curr_step = 0
        self.moves = np.zeros((self.dim, self.no_of_steps), dtype = np.int)

    def next(self, axis, pos):
        ch = []
        if pos - 1 >= np.int(self.bounds[axis][0]):
            ch.append(-1)
        if pos + 1 <= np.int(self.bounds[axis][1]):
            ch.append(1)

        if len(ch) == 0:
            return 0
        else:
            return choice(ch)

    def walk(self, no_of_steps = None):
        if type(no_of_steps) in [int, np.int32, np.int64]:
            self.no_of_steps = no_of_steps
        for ax in range(self.dim):
            if self.unbounded[ax]:
                self.moves[ax] = 2 * (np.random.randint(2, size = self.no_of_steps) - 0.5)
            elif not self.confined[ax]:
                curr = 0
                while curr < self.no_of_steps:
                    pos = self.get_position(axis = ax, step = curr)[0]
                    free_walk = self.get_no_of_free_walk_moves(pos, \
                                                                self.bounds[ax], \
                                                                curr, \
                                                                self.no_of_steps)
                    if free_walk > 0:
                        self.moves[ax][curr : curr + free_walk] = \
                            np.array(2 * (np.random.randint(2, size = free_walk) - 0.5), dtype = np.int)
                        curr += free_walk
                    else:
                        self.moves[ax][curr] = self.next(ax, pos)
                        curr += 1
        return

    def get_no_of_free_walk_moves(self, current_position, bounds: tuple, current_step, total_no_of_steps):
        temp_1 = total_no_of_steps - current_step
        temp_2 = current_position - bounds[0]
        temp_3 = bounds[1] - current_position

        return np.int(min(temp_1, temp_2, temp_3))

    def get_position(self, axis = None, step = None):
        if axis is None:
            axis = np.linspace(1, self.dim, self.dim, dtype = np.int)
        elif type(axis) in [int, np.int32, np.int64]:
            axis = np.array([axis])
        elif axis is list:
            axis = np.array(axis)
        elif type(axis) is not np.ndarray:
            raise ValueError

        if step is None:
            step = -1

        pos = []

        for ax in axis:
            if self.confined[ax]:
                pos.append(self.start_position[ax])
            else:
                no_of_positives = np.sum(self.moves[ax, 0:step] > 0)
                pos.append(2 * no_of_positives - step + self.start_position[ax])

        return np.array(pos)
        
    def get_evolution(self, axis = None):

        if axis is None:
            axis = np.linspace(0, self.dim - 1, self.dim, dtype = np.int)
        elif type(axis) in [int, np.int32, np.int64]:
            axis = np.array([axis])
        elif axis is list:
            axis = np.array(axis)
        elif type(axis) is not np.ndarray:
            raise ValueError

        evolution = np.zeros((axis.shape[0], self.no_of_steps + 1))

        for ax in axis:
            evolution[ax][0] = self.start_position[ax]
            if self.confined[ax]:
                evolution[ax] = self.start_position[ax] * np.ones(self.time.shape[0])
                continue
            for t in self.time[1:]:
                evolution[ax][t] = evolution[ax][t - 1] + self.moves[ax][t - 1]
        
        return evolution

if __name__ == "__main__":
    no_of_steps = 1e3
    dim = 3
    bounds = [(10, 100), None, (1, 1)]

    wlk = Walker(no_of_steps = no_of_steps, dim = dim, bounds = bounds)

    print(wlk.start_position)

    