from copy import deepcopy
import numpy as np

class Metric:

    def __init__(self, metric: callable, coordinate_origin, name = None, description = None):
        self.name = name
        self.description = description
        self.update_metric(metric, coordinate_origin)

    def update_metric(self, metric: callable, coordinate_origin):
        self.metric = metric
        self.coordinate_origin = coordinate_origin

    def print_data(self, stream):
        stream.write(str(self))

    def __add__(self, other):
        ret = deepcopy(other)
        def new_metric(a, b):
            return self.metric(a, b) + other.metric(a, b)
        ret.update_metric(new_metric, other.coordinate_origin)
        return ret
        
    def __sub__(self, other):
        ret = deepcopy(other)
        def new_metric(a, b):
            return self.metric(a, b) - other.metric(a, b)
        ret.update_metric(new_metric, other.coordinate_origin)
        return ret

    def __mul__(self, other):
        ret = deepcopy(other)
        def new_metric(a, b):
            return self.metric(a, b) * other.metric(a, b)
        ret.update_metric(new_metric, other.coordinate_origin)
        return ret

    def __call__(self, first, second = None):
        if first is None:
            first = self.coordinate_origin
        if second is None:
            second = self.coordinate_origin
        return self.metric(first, second)

    def __str__(self):
        ret = "\tMetric function"
        if self.name is not None:
            ret += ": " + str(self.name)
        if self.description is not None:
            ret += "\n\tDescription: " + str(self.description)
        ret += "\n\tCoordinate origin: " + str(self.coordinate_origin)
        return ret

    def metric_data(self):
        yield "Name: " + str(self.name)
        yield "Description: " + str(self.description)
        yield "Coordinate Origin: " + str(self.coordinate_origin)

class InnerProductL2:

    def __init__(self):
        pass

    def check(self, a: np.ndarray, b:np.ndarray):
        if len(a.shape) != 1 or len(b.shape) != 1:
            return False
        return a.shape[0] == b.shape[0]

    def __call__(self, a: np.ndarray, b: np.ndarray):
        if self.check(a, b):
            return np.sum(a * b)
        else:
            print(a, b)
            return np.nan