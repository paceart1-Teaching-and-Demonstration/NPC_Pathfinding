import math
import json


class Node:
    def __init__(self, name, loc: tuple, is_key):
        self.name = name
        self.location = loc
        self.is_key = is_key
        self.neighbors = {}

    def add_neighbor(self, node_name, weight):
        """

        :param node_name:
        :param weight:
        :return:
        """
        if node_name in self.neighbors:
            raise Exception(f"Neighbor ref already exists between {self.name} and {node_name}")
        self.neighbors[node_name] = weight


class Map:
    def __init__(self, background_file=None, paths_file=None):
        self.Nodes = {}
        self.background_file = background_file
        self.paths_file = paths_file

        if self.paths_file is not None:
            self._load_map_data()

    def _load_map_data(self):
        """

        :return:
        """
        file = open(self.paths_file, "r")
        map_data_json = json.load(file)
        file.close()
        nodes = map_data_json['nodes']
        paths = map_data_json['paths']

        for n in nodes:
            name = n['name']
            loc = tuple(n['location'])
            isKey = n['isKey']
            self.add_node(name, loc, isKey)
            # self.add_Node("Outside_main", (242, 490), 1)

        for p in paths:
            start = p['start']
            end = p['end']
            weight_mult = p['weight']
            dist = math.dist(self.Nodes[start].location, self.Nodes[end].location)
            total_weight = dist * weight_mult
            self.add_node_connections(start, end, total_weight)
            # self.add_node_connections("Garden_entr", {"Garden_int1": 1})

    def add_node(self, name, loc, is_key_loc=0):
        """

        :param name:
        :param loc:
        :param is_key_loc:
        :return:
        """
        if name in self.Nodes:
            raise Exception("A Node with that name already exists")
        self.Nodes[name] = Node(name, loc, is_key_loc)

    def add_node_connections(self, node_name, connection, total_weight):
        """

        :param node_name:
        :param connection:
        :param total_weight:
        :return:
        """
        if node_name not in self.Nodes:
            raise Exception(f"No node exists with the name {node_name}")

        self.Nodes[node_name].add_neighbor(connection, total_weight)

    def get_key_nodes(self):
        """

        :return:
        """
        key_nodes = []
        for n in self.Nodes.keys():
            if self.Nodes[n].is_key:
                key_nodes.append(n)
        return key_nodes

      
if __name__ == "__main__":
    pass
     