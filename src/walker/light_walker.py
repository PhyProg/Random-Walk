import numpy as np 
from random import choice

def default_choice(possible_states, **kwargs):
    return choice(possible_states)

class LightWalker:

    def __init__(self,
                next_step_processor = default_choice, 
                data_collection_keys = [], 
                dim = 3, 
                initial_position = None,
                max_no_of_steps = 1e8):

        self.next_step_processor = next_step_processor
        self.dim = dim
        self.max_no_of_steps = np.int64(max_no_of_steps)
        self.terminated = False
        if initial_position is None:
            initial_position = np.zeros(self.dim, dtype = np.int64)
        self.visited = np.zeros((self.max_no_of_steps, dim), dtype = np.int64)
        self.visited[0] = initial_position
        self.reset()
        for key in data_collection_keys:
            self.data[key] = []

    def reset(self):
        self.step = 0
        self.data = {}

    def get_current_coordinate(self):
        return self.visited[self.step]

    def walk(self, possible_states: list, **kwargs):
        if not self.terminated:
            next = self.next_step_processor(possible_states, **kwargs)
            self.step += 1
            self.visited[self.step] = np.array(next)
        if self.step >= self.max_no_of_steps:
            self.terminated = True

    def add_data(self, data_key: str, value: np.ndarray):
        self.data[data_key].append(value)

    def get_visited_coordinates(self, axis = None, termination = None):
        
        if termination is None or termination > self.step:
            termination = self.step
        
        if axis is None:
            return self.visited[:termination]
        elif type(axis) in [int, np.int32, np.int64] and axis < self.dim:
            return self.visited[:termination, axis]
        else:
            raise ValueError

    def get_position(self, time = None, axis = None):
        
        if time is None or time > self.step or time < 0:
            time = self.step
        
        if axis is None:
            return self.visited[time]
        elif type(axis) in [int, np.int32, np.int64] and axis < self.dim:
            return self.visited[time, axis]
        else:
            raise ValueError


if __name__ == "__main__":
    lw = LightWalker(max_no_of_steps=10, data_collection_keys=['data'])

    for i in range(5):
        lw.walk([[1, 2, 3], [2, 3, 4], [1, 2, 3]])
        lw.add_data('data', 123)

    print(lw.__dict__)
    print(lw.get_position(axis = np.int64(1), time= 2))
