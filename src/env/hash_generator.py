import numpy as np

class HashGenerator:

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

    def __call__(self, coordinates: np.array):
        return self.coord_to_hash(coordinates = coordinates)

    def coord_to_hash(self, coordinates: np.array or list, max_coord = 1e6):
        if coordinates is list:
            coordinates = np.array(coordinates)
        try:
            max_coord = self.max_coord
        except: AttributeError
        ret = ""
        dim = len(str(2*max_coord))
        for coord in coordinates:
            temp = int(max_coord + coord)
            l = len(str(temp))
            st = ""
            for i in range(dim - l):
                st += "0"
            ret += st + str(temp) + "-"
        return ret[:-1]

    def hash_to_coord(self, hash: str, max_coord = 1e6):
        try:
            max_coord = self.max_coord
        except: AttributeError
        coords = hash.split("-")
        ret = []
        for coord in coords:
            ret.append(int(coord) - max_coord)
        return np.array(ret)