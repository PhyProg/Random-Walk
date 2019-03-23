class DataProcessor:

    def __init__(self, key_to_be_collected: str, processor: callable, **kwargs):
        self.key_to_be_collected = key_to_be_collected
        self.processor = processor
        self.processor_default_params = {}
        self.has_default_params = False

        #kwargs should be parameters of processor function

        for key, value in kwargs.items():
            self.has_default_params = True
            self.processor_default_params[key] = value

    def __call__(self, *args, **kwargs):
        if kwargs:
            return self.processor(*args, **kwargs)
        elif self.has_default_params:
            try:
                return self.processor(*args, **self.processor_default_params)
            except: ValueError
        else:
            raise ValueError

    
def p_mean_calculator(key, p = 1):
    import numpy as np
    def pr(data: np.ndarray or list, p = 1):
        data = np.array(data)
        return np.mean(data ** p) ** (1 / p)
    
    processor = DataProcessor(key_to_be_collected = key, processor = pr, p = 1)
    
    return processor

def p_sum_calculator(key, p = 1):
    import numpy as np
    def pr(data: np.ndarray or list, p = 1):
        data = np.array(data)
        return np.sum(data ** p)
    
    processor = DataProcessor(key_to_be_collected = key, processor = pr, p = 1)

    return processor
