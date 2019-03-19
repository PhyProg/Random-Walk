from node import Node
from graph import *
from metric import Metric
from metric_graph import MetricGraph

import numpy as np
import sys

def metric_2(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.sqrt(np.sum((a - b)**2))

node = Node(coord = np.zeros(2), x = 121)

metric = Metric(metric_2, np.zeros(3), name = "2-norm", description = '2-norm')

metric_graph = MetricGraph(metric)

metric_graph.add_node(node)

metric_graph.add_node(Node(x = 1))

metric_graph.feed_node_norms()

metric_graph.print_data(sys.stdout, default_startswith = "")
