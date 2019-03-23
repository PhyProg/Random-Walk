from random import choice

class Walker:

    def __init__(self, is_processing_data = False, 
                    data_processors = [],
                    keys_to_collect = [],
                    is_processor_same_for_all_data = False):
        
        self.reset()
        self.is_processing_data = is_processing_data
        self.keys_to_collect = keys_to_collect
        self.is_processor_same_for_all_data = is_processor_same_for_all_data
        if self.is_processor_same_for_all_data:
            self.data_processors = data_processors[0]
        else:
            self.data_processors = data_processors

        for key in self.keys_to_collect:
            self.data[key] = []

    def return_results(self, keys = []):
        ret = []
        if self.is_processor_same_for_all_data:
            for key in keys:
                ret.append(self.data_processors(self.data[key]))
        else:
            for key, processor in zip(keys, self.data_processors):
                ret.append(processor(self.data[key]))
        return ret

    def reset(self):
        self.step = 0
        self.visited = []
        self.data = {}
        self.is_processing_data = False
        self.is_processor_same_for_all_data = False
        self.data_processors = []
        self.keys_to_collect = []

    def next(self, possible_states):
        return choice(possible_states)

    def walk(self, next_pos_id):
        self.step += 1
        self.visited.append(next_pos_id)

    def collect_data(self, node = None, data_dict = None):
        if node is not None:
            for key in self.keys_to_collect:
                if key in node.__dict__.keys():
                    self.data[key].append(node.__dict__[key])
            return
        elif data_dict is dict:
            for key in self.keys_to_collect:
                if key in data_dict.keys():
                    self.data[key].append(data_dict[key])
            return
        else:
            return

if __name__ == "__main__":
    walker = Walker(is_processing_data=True, data_processors=[1], keys_to_collect=["a", "b"], is_processor_same_for_all_data=True)
    print(walker.__dict__)