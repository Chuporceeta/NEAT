import math
import random

from Node import Node
from Connection import Connection
import turtle as t

initial_mutation_chance = 0.6


class Network:
    def __init__(self, population, inputs, outputs, connections=None):
        self.__population = population
        self.__nodes = inputs + outputs
        self.__layers = []
        self.divide_into_layers()
        if connections is None:
            self.__connections = []
            for i in range(len(inputs) * len(outputs)):
                if random.random() < initial_mutation_chance:
                    self.mutate_connection()
        else:
            self.__connections = connections

    def sort_nodes(self):
        """Sort node by layer."""
        self.__nodes.sort(key=lambda n: n.layer)

    def divide_into_layers(self):
        self.sort_nodes()
        last_layer_num = 0
        curr_layer = []
        self.__layers = []
        for node in self.__nodes:
            if node.layer == last_layer_num:
                curr_layer.append(node)
            else:
                self.__layers.append(curr_layer)
                curr_layer = [node]
            last_layer_num = node.layer
        self.__layers.append(curr_layer)

    def is_fully_connected(self):
        max_connections = 0
        num_nodes_before = len(self.__layers[0])
        for i in range(1, len(self.__layers)):
            max_connections += num_nodes_before * len(self.__layers[i])
            num_nodes_before += len(self.__layers[i])
        return max_connections == len(self.__connections)

    def mutate_node(self):
        connection = self.__connections[random.randint(0, len(self.__connections) - 1)]
        while not connection.is_enabled():
            connection = self.__connections[random.randint(
                0, len(self.__connections) - 1)]

        node_in = connection.node_in
        node_out = connection.node_out
        weight = connection.weight

        new_node = Node(node_in.layer + 1)
        in_connection = Connection(node_in, new_node, 1)
        self.__population.set_innovation_number(in_connection)
        out_connection = Connection(new_node, node_out, weight)
        self.__population.set_innovation_number(out_connection)
        print(f'Created node {new_node}, splitting connection {connection},\n'
              f'and creating {in_connection} and {out_connection}')

        connection.disable()

        def cascade_layer_increment(node):
            """When increasing node layer, increase layers of nodes connected
            after, where necessary"""
            for connection in self.__connections:
                if (connection.node_in == node and
                        connection.node_out.layer == node.layer):
                    connection.node_out.layer += 1
                    cascade_layer_increment(connection.node_out)

        if node_out.layer == new_node.layer:
            node_out.layer += 1
            cascade_layer_increment(node_out)
        self.__nodes.append(new_node)
        self.__connections.append(in_connection)
        self.__connections.append(out_connection)
        self.divide_into_layers()

    def mutate_connection(self):
        if self.is_fully_connected():
            print('Could not add connection: Network is fully connected')
            return False
        node_in = self.__nodes[random.randint(0, len(self.__nodes) - 1)]
        node_out = self.__nodes[random.randint(0, len(self.__nodes) - 1)]

        # Can't connect within same layer or if already connected
        while node_in.layer == node_out.layer \
                or node_in.is_connected_to(node_out):
            node_in = self.__nodes[random.randint(0, len(self.__nodes) - 1)]
            node_out = self.__nodes[random.randint(0, len(self.__nodes) - 1)]

        # Make sure the connection points forward
        if node_in.layer > node_out.layer:
            node_in, node_out = node_out, node_in
        weight = random.uniform(-1, 1)
        connection = Connection(node_in, node_out, weight)
        self.__population.set_innovation_number(connection)
        self.__connections.append(connection)
        print(f'Added connection {connection}')
        return True

    def connect_nodes(self):
        for node in self.__nodes:
            node.clear_inputs()
        for connection in self.__connections:
            node_out = connection.node_out
            node_out.add_input(connection)

    def propagate(self):
        self.connect_nodes()
        self.sort_nodes()
        for node in self.__nodes:
            if node.layer != 0:
                node.activate()
        print(self.__nodes[-1].value)

    def print_network(self):
        for connection in self.__connections:
            print(connection)

    def display_network(self):
        self.connect_nodes()
        layers = self.__layers
        x_scale = 10 / (1 + len(layers) // 8)
        w = x_scale * (len(layers) - 1)
        h = 10 * (max(len(layer) for layer in layers) - 1)
        t.setup(20 * w, 20 * h)
        t.setworldcoordinates(-5, -h / 2 - 5, w + 5, h / 2 + 5)
        t.clear()
        t.penup()
        t.speed(0)
        t.hideturtle()

        node_coords = []
        for layer in layers:
            temp = []
            for i, node in enumerate(layer):
                layer_num = node.layer
                x = layer_num
                if layer_num == 0 or layer_num == len(layers) - 1:
                    y = math.ceil(i + 1 - (len(layer) + 1) / 2)
                else:
                    y_sum = 0
                    for connection in node.inputs:
                        if connection.is_enabled():
                            node_in = connection.node_in
                            y_sum += node_coords[node_in.layer][layers[
                                node_in.layer].index(node_in)][1] \
                                # * abs(connection.weight)
                    y = y_sum / (len(node.inputs) + 2)
                    if -0.08 <= y <= 0.08:
                        y += random.choice((-1, 1)) * random.uniform(
                            0.1 + i / 20,
                            0.35 + i / 20)
                temp.append([x, y, node.num])
            node_coords.append(temp)

        for connection in self.__connections:
            if connection.is_enabled():
                node_in = connection.node_in
                node_out = connection.node_out
                weight = connection.weight
                in_coords = node_coords[node_in.layer][layers[node_in.layer]
                .index(node_in)]
                out_coords = node_coords[node_out.layer][layers[node_out.layer]
                .index(node_out)]
                t.goto(x_scale * in_coords[0], 10 * in_coords[1])
                t.pendown()
                if weight < 0:
                    t.color('red')
                t.width(abs(weight) * 3)
                t.goto(x_scale * (in_coords[0] + out_coords[0]) / 2,
                       10 * (in_coords[1] + out_coords[1]) / 2)
                t.color('teal')
                t.write(connection.innov)
                t.color('red' if weight < 0 else 'black')
                t.goto(x_scale * out_coords[0], 10 * out_coords[1])
                t.penup()
                t.color('black')

        for layer in node_coords:
            for coords in layer:
                t.goto(x_scale * coords[0], 10 * coords[1])
                t.dot(10)
                t.color('teal')
                t.write(coords[2])
                t.color('black')
