import numpy as np 
from random import choice

class LightWalker:

    def __init__(self, data_collection_keys = [], 
                data_shape = [], 
                data_type = [], 
                dim = 3, 
                initial_position = None,
                max_no_of_steps = 1e8):

        self.dim = dim
        self.max_no_of_steps = np.int64(max_no_of_steps)
        self.terminated = False
        if initial_position is None:
            initial_position = np.zeros(self.dim, dtype = np.int64)
        self.visited = np.zeros((self.max_no_of_steps, dim), dtype = np.int64)
        self.visited[0] = initial_position
        self.reset()
        for key, shape, type in zip(data_collection_keys, data_shape, data_type):
            self.data[key] = np.zeros(shape, dtype = type)

    def reset(self):
        self.step = 0
        self.data = {}

    def walk(self, possible_states: list):
        if not self.terminated:
            next = choice(possible_states)
            self.step += 1
            self.visited[self.step] = np.array(next)
            print(self.visited[:self.step])
        if self.step >= self.max_no_of_steps:
            self.terminated = True

    def add_data(self, data_key: str, value: np.ndarray):
        self.data[data_key] = np.append(self.data[data_key], value)

    def get_visited_coordinates(self, axis = None, termination = None):
        
        if termination is None:
            termination = self.step
        elif termination > self.step:
            termination = self.step
        
        if axis is None:
            return self.visited[:termination]
        elif type(axis) in [int, np.int32, np.int64] and axis < self.dim:
            return self.visited[:termination, axis]
        else:
            raise ValueError

if __name__ == "__main__":
    lw = LightWalker(max_no_of_steps=10)

    for i in range(5):
        lw.walk([[1, 2, 3], [2, 3, 4], [1, 2, 3]])

    print(lw.__dict__)
    print(lw.get_visited_coordinates(axis = np.int64(1), termination = 2))
