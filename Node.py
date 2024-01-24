import math

sigmoid = lambda x: 1 / (1 + math.e ** (-4.9 * x))


class Node:
    num_nodes = 1

    def __init__(self, layer, value=0, activation_func=sigmoid):
        self.__layer = layer
        self.__value = value
        self.__inputs = []
        self.__num = Node.num_nodes
        self.__activation_func = activation_func
        Node.num_nodes += 1

    def activate(self):
        weighted_sum = 0
        for connection in self.__inputs:
            if connection.is_enabled():
                node_in = connection.node_in
                weight = connection.weight
                weighted_sum += node_in.value * weight
        self.__value = self.__activation_func(weighted_sum)

    def is_connected_to(self, other):
        for connection in self.__inputs:
            if connection.node_in == other:
                return True
        for connection in other.inputs:
            if connection.node_in == self:
                return True
        return False

    def clear_inputs(self):
        self.__inputs.clear()

    def add_input(self, connection):
        self.__inputs.append(connection)

    @property
    def value(self):
        return self.__value

    @property
    def num(self):
        return self.__num

    @property
    def inputs(self):
        return self.__inputs

    @property
    def layer(self):
        return self.__layer

    @layer.setter
    def layer(self, layer):
        self.__layer = layer

    def __repr__(self):
        return f'{self.__num}[l{self.__layer}]'
