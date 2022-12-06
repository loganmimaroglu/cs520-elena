import osmnx as ox
import networkx as nx
import os
from dotenv import load_dotenv
from IPython.display import IFrame
import geopandas as gpd
import sys
import math
import numpy as np

class Model(object):

    def __init__(self):
        self.filepath = "./data/piedmont.graphml"
    def osm_network(self):
        """
        Builds an Open Street Maps network of Amherst, MA and uses Google's Elevation API
        to add an elevation attribute which represents meters above see level.
        The OSM network is stored locally in a GraphML file.
        If the file already exists it loads the file.
        :return: g networkx.MultiDiGraph
        """
        if os.path.exists(self.filepath):
            return ox.load_graphml(self.filepath)

        g = ox.graph_from_place("Natick, Massachusetts, USA", network_type="walk")

        try:
            load_dotenv()

            google_elevation_api_key = os.getenv('google_elevation_api_key')

            g = ox.add_node_elevations_google(g, api_key=google_elevation_api_key)
            g = ox.add_edge_grades(g, add_absolute=True)

            ox.save_graphml(g, self.filepath)

        except ImportError:
            print("You need a google_elevation_api_key in your .env to run this.")

        return g

    # TODO: This should be moved to view/controller
    def display(self, origin, destination):
        G = self.osm_network()

        # nc = ox.plot.get_node_colors_by_attr(G, "elevation", cmap="plasma")
        # fig, ax = ox.plot_graph(G, node_color=nc, node_size=20, edge_linewidth=2, edge_color="#333")
        m1 = ox.plot_graph_folium(G, popup_attribute="name", weight=2, color="#8b0000")
        m1.save("./data/graph.html")
        IFrame("../data/graph.html", width=600, height=500)

        route = self.shortest_path(origin, destination)

        m2 = ox.plot_route_folium(G, route, route_map=m1, popup_attribute="length", weight=7)
        m2.save("./data/route_graph.html")
        IFrame("../data/route_graph.html", width=600, height=500)



    # This uses the built in shortest path algo
    def shortest_path_and_length(self, origin, destination):
        G = self.osm_network()

        # Convert lat/long to nodes on graph
        orig_node = ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0])
        dest_node = ox.distance.nearest_nodes(G, X=destination[1], Y=destination[0])
        shortest_path = nx.shortest_path(G, orig_node, dest_node, weight="length")
        return nx.shortest_path_length(G, orig_node, dest_node, weight="length"),shortest_path

    # Dijkstra or/and A*
    def shortest_path_dijkstra(self, origin, destination, scale):
        G = self.osm_network()
        nodes, edges = ox.graph_to_gdfs(G)
        # print(nodes.iloc[:,0:2][100:150])
        min_length = edges['length'].min()
        # print(nodes.columns.values)
        # print(edges['grade'])
        shortest_length,shortest_path = self.shortest_path_and_length(origin, destination)
        diff = shortest_length*(scale - 1)
        # print(min_length, math.ceil(diff/min_length),diff)
        threshold = len(shortest_path) + math.ceil(diff/min_length)
        paths = self.all_paths(origin, destination, threshold)
        target_length = scale*shortest_length
        count = 0
        filtered_paths = []
        # print(shortest_length)
        # TODO: fix filtering
        for path in paths:
            temp_length = 0
            for i in range(len(path)-1):
                u  = path[i]
                v = path[i+1]
                temp_length +=  G.adj[u][v][0]['length']
                if(temp_length > target_length):
                    break
            if(shortest_length <= temp_length <= target_length):
                # print(temp_length, target_length)
                filtered_paths.append(path)
            count +=1
        print('number of paths before filtering:{}'.format(count))
        return filtered_paths
        
    def maximize_elevation_path(self, origin, destination, scale):
        G = self.osm_network()

        filtered_paths = self.shortest_path_dijkstra(origin, destination, scale)
        print('number of paths after filtering:{}'.format(len(filtered_paths)))

        highest_average_grade_path = max(filtered_paths, key=lambda path: np.mean(ox.utils_graph.get_route_edge_attributes(G, path, "grade_abs")))
        self.print_route_stats(highest_average_grade_path)

        return max(filtered_paths, key=lambda path: np.mean(ox.utils_graph.get_route_edge_attributes(G, path, "grade_abs")))

    def all_paths(self,origin, destination, threshold):
        G = self.osm_network()
        orig_node = ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0])
        dest_node = ox.distance.nearest_nodes(G, X=destination[1], Y=destination[0])
        return nx.all_simple_paths(G,orig_node, dest_node, cutoff=threshold)

    def print_route_stats(self, route):
        G = self.osm_network();

        route_grades = ox.utils_graph.get_route_edge_attributes(G, route, "grade_abs")
        msg = "The average grade is {:.1f}% and the max is {:.1f}%"
        print(msg.format(np.mean(route_grades) * 100, np.max(route_grades) * 100))

        route_lengths = ox.utils_graph.get_route_edge_attributes(G, route, "length")
        print("Total trip distance: {:,.0f} meters".format(np.sum(route_lengths)))