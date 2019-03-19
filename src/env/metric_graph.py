from graph import *

class MetricGraph(Graph):

    def __init__(self, metric: callable):
        self.metric = metric
        self.coord_origin = self.metric.coordinate_origin
        super(MetricGraph, self).__init__()
        return

    def feed_node_norms(self):
        for node in self.nodes.values():
            node.add_arguments(norm = self.metric(node.metric_args()))
        return

    def print_data(self, stream, default_startswith = ""):
        super(MetricGraph, self).print_data(stream, default_startswith = default_startswith)
        self.print_metric_data(stream, default_startswith = default_startswith + "\t")
        return

    def print_metric_data(self, stream, default_startswith = ""):
        stream.write(default_startswith + "Metric:" + "\n")
        for data in self.metric.metric_data():
            stream.write(default_startswith + "\t" + data + "\n")
        return
