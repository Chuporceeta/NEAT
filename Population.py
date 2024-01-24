from Connection import Connection
from Network import Network
from Node import Node
import turtle as t


class Population:
    def __init__(self):
        self.__global_innovation_num = 0
        self.__networks = []
        self.__innovations = []

    def set_innovation_number(self, connection):
        if connection not in self.__innovations:
            self.__global_innovation_num += 1
            connection.innov = self.__global_innovation_num
            self.__innovations.append(connection)
        else:
            connection.innov = self.__innovations[self.__innovations.index(connection)].innov


def main():
    pop = Population()
    inputs = [Node(0, 1), Node(0, 0.5), Node(0, 0.3)]
    outputs = [Node(1)]
    network = Network(pop, inputs, outputs)
    network.display_network()

    def n():
        network.mutate_node()
        network.display_network()

    def c():
        network.mutate_connection()
        network.display_network()

    t.onkey(n, 'n')
    t.onkey(c, 'c')
    t.onkey(lambda: network.print_network(), 'p')
    t.onkey(lambda: network.display_network(), 'r')
    t.listen()
    t.mainloop()


main()
