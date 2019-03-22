class Node:

    #Initialization. 
    def __init__(self, **kwargs):
        self.node_id = None 
        self.next_ids = []
        self.prev_ids = []
        self.add_arguments(**kwargs)

    def metric_args(self):
        try:
            return self.__dict__[self.metric_arg_key]
        except AttributeError: 
            return None

    def add_arguments(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key] = kwargs[key]

    def update_node_id(self, id):
        self.node_id = id

    def remove_id(self, id):
        self.remove_next_id(id)
        self.remove_prev_id(id)

    def remove_prev_id(self, id):
        if id in self.prev_ids:
            self.prev_ids.remove(id)

    def remove_next_id(self, id):
        if id in self.next_ids:
            self.next_ids.remove(id)

    def print_data(self, stream, default_startswith = ""):
        stream.write(default_startswith + "Node:" + "\n")
        for data in self.node_data():
            stream.write(default_startswith + "\t" + data + "\n")

    def node_data(self):
        yield "Node Id: " + str(self.node_id)
        yield "Next Nodes Id: \n"
        for next_id in self.next_ids:
            yield "\t" + next_id
        yield "Prev Nodes Id: \n"
        for prev_id in self.prev_ids:
            yield "\t" + prev_id
        for key in self.__dict__.keys() - {'node_id', 'next_ids', 'prev_ids'}:
            yield key + ": " + str(self.__dict__[key])
        return

    def __str__(self):
        ret = ""
        temp = list(self.node_data())
        for _ in temp:
            ret += _ + "\n"
        return ret
        
