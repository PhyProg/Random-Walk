import numpy as np

class LightGrid:

    def __init__(self, bounded = False, dr = None, dim = 3, **kwargs):
        self.dim = dim
        if dr is None:
            self.dr = np.ones(self.dim, dtype = np.int64)
        if bounded:
            if 'bounds' not in kwargs.keys():
                raise AttributeError("If grid is bounded you need to provide bounds")
            else:
                self.bounded = []
                if 'bounded_axis' in kwargs.keys():
                    if len(list(kwargs['bounded_axis'])) != dim:
                        raise ValueError("You must provide indicator for each axis")
                    else:
                        bd = np.array(kwargs['bounded_axis']) > 0
                        sum = np.sum(bd)
                        if sum != len(list(kwargs['bounds'])):
                            raise ValueError("You must provide equal number of indicators and bounds")
                        else:
                            self.bounded = [False for i in range(dim)]
                            idx = np.where(bd > 0)
                            self.bounded_indices = idx[0]
                            for id in idx[0]:
                                self.bounded[id] = True
                else:
                    self.bounded.extend(True for bound in kwargs['bounds'])
                    self.bounded.extend(False for i in range(dim - len(self.bounded))) 
                self.bounds = {}
                for i in range(self.bounded_indices.shape[0]):
                    self.bounds[str(self.bounded_indices[i])] = kwargs['bounds'][i]
                kwargs.pop('bounds')
        
        self.__dict__['wormholes'] = {}
        self.__dict__['blackholes'] = []

        if 'wormholes' in kwargs.keys():
            for wormhole in kwargs['wormholes']:
                self.add_wormhole(wormhole[0], wormhole[1])
            kwargs.pop('wormholes')

        if 'blackholes' in kwargs.keys():
            for blackhole in kwargs['blackholes']:
                self.add_blackhole(blackhole)
            kwargs.pop('blackholes')

        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

    def add_blackhole(self, hole):
        try:
            hole = np.array(hole)
        except: ValueError
        self.blackholes.append(str(hole))

    def add_wormhole(self, first, second, one_way = False):
        try:
            first = np.array(first)
            second = np.array(second)
        except: ValueError
        if str(first) not in self.wormholes.keys():
            self.wormholes[str(first)] = []
        self.wormholes[str(first)].append(second)
        if not one_way:
            if str(second) not in self.wormholes.keys():
                self.wormholes[str(second)] = []
            self.wormholes[str(second)].append(first)

    def next(self, current: np.ndarray):
        possible_pos = []
        if str(current) in self.blackholes:
            return [current]
        if str(current) in self.wormholes.keys():
            return self.wormholes[str(current)]
        for i in range(self.dim):
            ddr = np.zeros(self.dim)
            ddr[i] = self.dr[i]
            for sign in [+1, -1]:
                temp = current + sign * ddr
                if i in self.bounded_indices:
                    if temp[i] > self.bounds[str(i)][0] and temp[i] < self.bounds[str(i)][1]:
                        possible_pos.append(temp)
                else:
                    possible_pos.append(temp)
        return possible_pos