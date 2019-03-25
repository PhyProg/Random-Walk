from hash_generator import HashGenerator
from metric import Metric
from metric_graph import MetricGraph
from node import Node 

import numpy as np 
import sys

def get_quadratic_grid_2d(x_l, x_r, y_l, y_r, d_x = 1, d_y = 1):
    max_coord = np.abs([x_l, x_r, y_l, y_r]).max()
    
    def _2_norm(a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    coord_origin = np.zeros(2)

    generator = HashGenerator(max_coord = max_coord)

    metric = Metric(metric = _2_norm, coordinate_origin = coord_origin, name = '2-norm metric', \
        description = 'Returns quadratic root of sum of squares of distances in every coordinate')
    
    graph = MetricGraph(metric = metric, id_generator = generator)

    x_coord = np.arange(x_l, x_r + d_x, d_x)
    y_coord = np.arange(y_l, y_r + d_y, d_y)

    for y in y_coord:
        for x in x_coord:
            node = Node(coordinates = np.array([x, y]), metric_arg_key = 'coordinates')
            graph.add_node(node, coordinates = np.array([x, y]))

    graph.feed_node_norms()

    #Edges

    xx = [x_l, x_r]
    yy = [y_l, y_r]

    sign = [1, -1]

    for i in range(2):
        for j in range(2):
            id_first = generator(np.array([xx[i], yy[j]]))
            id_second = generator(np.array([xx[i] + sign[i] * d_x, yy[j]]))
            graph.add_connection(first = id_first, second = id_second)
            id_second = generator(np.array([xx[i], yy[j] + sign[j] * d_y]))
            graph.add_connection(first = id_first, second = id_second)

    #Sides

    for i in range(2):
        for j in range(1, x_coord.shape[0] - 1):
            id_first = generator(np.array([x_coord[j], yy[i]]))
            id_second = generator(np.array([x_coord[j] - d_x, yy[i]]))
            graph.add_connection(first = id_first, second = id_second)
            id_second = generator(np.array([x_coord[j] + d_x, yy[i]]))
            graph.add_connection(first = id_first, second = id_second)
            id_second = generator(np.array([x_coord[j], yy[i] + sign[i] * d_y]))
            graph.add_connection(first = id_first, second = id_second)

    for j in range(2):
            for i in range(1, y_coord.shape[0] - 1):
                id_first = generator(np.array([xx[j], y_coord[i]]))
                id_second = generator(np.array([xx[j], y_coord[i] - d_y]))
                graph.add_connection(first = id_first, second = id_second)
                id_second = generator(np.array([xx[j], y_coord[i] + d_y]))
                graph.add_connection(first = id_first, second = id_second)
                id_second = generator(np.array([xx[j] + sign[j] * d_x, y_coord[i]]))
                graph.add_connection(first = id_first, second = id_second)

    #Inside

    for i in range(1, y_coord.shape[0] - 1):
        for j in range(1, x_coord.shape[0] - 1):
            #print(i, j)
            id_first = generator(np.array([x_coord[j], y_coord[i]]))
            neighbours = around(x_coord[j], y_coord[i], d_x = d_x, d_y = d_y)
            for neighbour in neighbours:
                id_second = generator(np.array(neighbour))
                graph.add_connection(first = id_first, second = id_second)

    #graph.print_data(sys.stdout)

    return graph

def around(x, y, d_x = 1, d_y = 1):
    return [(x - d_x, y), (x + d_x, y), (x, y - d_y), (x, y + d_y)]

def get_quadratic_grid_dd(bounds: list, dr = None):
    dim = len(bounds)
    if dr is None:
        dr = np.ones(dim, dtype = np.int64)
    coords = [np.arange(bounds[i][0], bounds[i][1], dr[i]) for i in range(dim)]

    coord_origin = np.zeros(dim, dtype = np.int64)
    generator = HashGenerator(max_coord = np.max([np.max(coords[i]) for i in range(dim)]))

    def _2_norm(a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    metric = Metric(metric = _2_norm, coordinate_origin = coord_origin, name = '2-norm metric', \
        description = 'Returns quadratic root of sum of squares of distances in every coordinate')
    
    graph = MetricGraph(metric = metric, id_generator = generator)

    for i in range(np.prod([coords[j].shape[0] for j in range(dim)])):
        curr = [el(coords, i, j) for j in range(dim)]
        temp_coords = np.array([coords[j][curr[j]] for j in range(dim)])
        node = Node(coordinates = temp_coords, metric_arg_key = 'coordinates')
        graph.add_node(node, coordinates = temp_coords)

    for i in range(np.prod([coords[j].shape[0] for j in range(dim)])):
        curr = [el(coords, i, j) for j in range(dim)]
        temp_coords = np.array([coords[j][curr[j]] for j in range(dim)])
        for ar in around_dd(temp_coords, bounds, dr = dr):
            graph.add_connection(first = generator(temp_coords), second = generator(ar))

    graph.feed_node_norms()
    return graph

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
    