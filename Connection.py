from Node import Node


class Connection:
    def __init__(self, node_in: Node, node_out: Node, weight: float):
        self.__node_in = node_in
        self.__node_out = node_out
        self.__weight = weight
        self.__enabled = True
        self.__innov = 0

    def disable(self):
        self.__enabled = False

    @property
    def innov(self):
        return self.__innov

    @innov.setter
    def innov(self, innov):
        self.__innov = innov

    @property
    def node_in(self):
        return self.__node_in

    @property
    def node_out(self):
        return self.__node_out

    @property
    def weight(self):
        return self.__weight

    def is_enabled(self):
        return self.__enabled

    def __eq__(self, other):
        return (self.__node_in.num == other.node_in.num
                and self.__node_out.num == other.node_out.num)

    def __repr__(self):
        return (f'({self.__node_in} ->'
                f' {self.node_out}, '
                f'{self.__weight * self.__enabled})')
