from IPython.display import IFrame
import osmnx as ox
import numpy as np
import networkx as nx
import math

class PathFindingView(object):

    def __init__(self):
        pass

    def get_route(self, route_map: nx.MultiDiGraph, orig: str, dest: str, grade: str = None, scale: float = None):
        # orig_node_id, dest_node_id = self.addresses_to_nodes(route_map, (orig, dest))
        orig_node_id, dest_node_id = orig, dest

        simple_paths_filtered = self.simple_paths_filtered(route_map, orig_node_id, dest_node_id, scale)

        if grade == "max":
            return max(simple_paths_filtered, key=lambda path: np.mean(ox.utils_graph.get_route_edge_attributes(route_map, path, "grade_abs")))
        elif grade == "min":
            return min(simple_paths_filtered, key=lambda path: np.mean(ox.utils_graph.get_route_edge_attributes(route_map, path, "grade_abs")))
        else:
            # return closest value
            pass


    def shortest_path_and_length(self, route_map, orig_node_id: int, dest_node_id: int) -> tuple[int, list[int]]:
        """
        Computes the path that minimizes the edge weight length and cumulative length of such a path.

        :param route_map: NetworkX graph
        :type: NetworkX graph
        :param orig_node_id: Starting node for path
        :type: int
        :param dest_node_id: Ending node for path
        :type: int
        :return: Return a single list of nodes id's in the shortest path from source to target
        :rtype: (int, list[int])
        """

        shortest_path = nx.shortest_path(route_map, orig_node_id, dest_node_id, weight="length")
        shortest_path_length = nx.shortest_path_length(route_map, orig_node_id, dest_node_id, weight="length")
        return shortest_path_length, shortest_path

    def simple_paths_filtered(self, route_map: nx.MultiDiGraph, orig_node_id: int, dest_node_id: int, scale: float):
        """
        Finds and returns a list of paths closest in length to the desired distance.

        :param route_map:
        :param orig_node_id:
        :param dest_node_id:
        :param grade:
        :param scale:
        :return:
        """
        nodes, edges = ox.graph_to_gdfs(route_map)

        min_len = edges['length'].min()

        shortest_path_len, shortest_path = self.shortest_path_and_length(route_map, orig_node_id, dest_node_id)
        diff = shortest_path_len * (scale - 1)

        threshold = len(shortest_path) + math.ceil(diff / min_len)
        print(threshold)

        paths = nx.all_simple_paths(route_map, orig_node_id, dest_node_id, cutoff=threshold)

        target_len = scale * shortest_path_len

        count = 0
        filtered_paths = []

        for path in paths:
            print(path)
            temp_len = 0
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                temp_len += route_map.adj[u][v][0]['length']

                if temp_len > target_len:
                    break

            if shortest_path_len <= temp_len <= target_len:
                filtered_paths.append(path)
            print(count)
            count += 1

        print('number of paths before filtering:{}'.format(count))
        return filtered_paths

    def addresses_to_nodes(self, route_map: nx.MultiDiGraph, addresses: tuple[str, str]) -> tuple[int, int]:
        """
        Converts address queries, i.e. "1 Presidents Dr, Amherst MA 01002" to the nearest nodes node IDs

        :param route_map: NetworkX graph
        :type: NetworkX graph
        :param addresses: A tuple of length 2 representing the start address and end address
        :type: (str, str)
        :return: a tuple of nearest node IDs
        :rtype: (int, int)
        """

        # Convert address to latitiude, longitude
        pos1_lat, pos1_lng = ox.geocode(addresses[0])
        pos2_lat, pos2_lng = ox.geocode(addresses[1])

        # Convert latitude, longitude to nodes in the graph
        pos1_node = ox.distance.nearest_nodes(route_map, X=pos1_lng, Y=pos1_lat)
        pos2_node = ox.distance.nearest_nodes(route_map, X=pos2_lng, Y=pos2_lat)

        return pos1_node, pos2_node

    def gps_to_nodes(self, route_map, orig_point, dest_point):
        pos1_lat, pos1_lng = orig_point[0], orig_point[1]
        pos2_lat, pos2_lng = dest_point[0], dest_point[1]

        pos1_node = ox.distance.nearest_nodes(route_map, X=pos1_lng, Y=pos1_lat)
        pos2_node = ox.distance.nearest_nodes(route_map, X=pos2_lng, Y=pos2_lat)

        return pos1_node, pos2_node

    # def display(self, route_map, origin, destination):
    #     # nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
    #     # fig, ax = ox.plot_graph(G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333")
    #     m1 = ox.plot_graph_folium(route_map, popup_attribute="name", weight=2, color="#8b0000")
    #     m1.save("./data/graph.html")
    #     IFrame("./data/graph.html", width=600, height=500)
    #
    #     route = self.shortest_path(origin, destination)
    #
    #     m2 = ox.plot_route_folium(route_map, route, route_map=m1, popup_attribute="length", weight=7)
    #     m2.save("./data/route_graph.html")
    #     IFrame("./data/route_graph.html", width=600, height=500)
    #
    # def print_route_stats(self, route_map, route):
    #
    #     route_grades = ox.utils_graph.get_route_edge_attributes(route_map, route, "grade_abs")
    #     msg = "The average grade is {:.1f}% and the max is {:.1f}%"
    #     print(msg.format(np.mean(route_grades) * 100, np.max(route_grades) * 100))
    #
    #     route_lengths = ox.utils_graph.get_route_edge_attributes(route_map, route, "length")
    #     print("Total trip distance: {:,.0f} meters".format(np.sum(route_lengths)))