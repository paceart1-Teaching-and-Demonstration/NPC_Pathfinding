# Dijkstra
from GameMap import Map
import heapq
import math


class Dijkstra:
    def __init__(self, node_map: Map):
        self.map = node_map

    def solve(self, start_name: str, stop_name: str):
        """

        :param start_name:
        :param stop_name:
        :return:
        """
        if start_name not in self.map.Nodes or stop_name not in self.map.Nodes:
            raise Exception("Invalid Start/Stop.  Name does not exists.")

        total_values = {m: math.inf for m in self.map.Nodes}
        forefront = []
        checked = []  # TODO: not in use
        connections = {}

        # init vals
        total_values[start_name] = 0
        heapq.heappush(forefront, (0, start_name))

        # solve
        while len(forefront):
            c_data = heapq.heappop(forefront)
            current_name = c_data[1]
            current_value = c_data[0]
            checked.append(current_name)
            neighbors = self.map.Nodes[current_name].neighbors
            if current_value > total_values[current_name]:
                continue
            for n in neighbors:
                v = neighbors[n] + current_value
                if v < total_values[n]:
                    connections[n] = current_name
                    total_values[n] = v
                    heapq.heappush(forefront, (v, n))

        path = []

        # no solution
        if total_values[stop_name] == math.inf:
            return path

        # backtrack path
        c = stop_name
        while True:
            path.append(self.map.Nodes[c].location)
            if c not in connections:
                break
            c = connections[c]
        path.reverse()

        return path


if __name__ == "__main__":
    
    game_map = Map()
    game_map.add_node("A", (300, 200))
    game_map.add_node("B", (100, 100))
    game_map.add_node("C", (100, 300))
    game_map.add_node("D", (100, 200))
    game_map.add_node_connections("A", "B", 5)
    game_map.add_node_connections("A", "C", 5)
    game_map.add_node_connections("B", "A", 10)
    game_map.add_node_connections("B", "D", 2)
    game_map.add_node_connections("C", "A", 5)
    game_map.add_node_connections("D", "B", 3)
    
    start = "C"
    end = "D"
    
    d = Dijkstra(game_map)
    print(d.solve(start, end))
