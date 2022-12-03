import osmnx as ox
import networkx as nx
import os
from dotenv import load_dotenv
from IPython.display import IFrame
import geopandas as gpd


class Model(object):

    def __init__(self):
        self.filepath = "../data/amherst.graphml"

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

        g = ox.graph_from_place("Amherst, Massachusetts, USA", network_type="bike")

        try:
            load_dotenv()

            google_elevation_api_key = os.getenv('google_elevation_api_key')

            g = ox.add_node_elevations_google(g, api_key=google_elevation_api_key)
            g = ox.add_edge_grades(g)

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
    def shortest_path(self, origin, destination):
        G = self.osm_network()

        # Convert lat/long to nodes on graph
        orig_node = ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0])
        dest_node = ox.distance.nearest_nodes(G, X=destination[1], Y=destination[0])

        return nx.shortest_path(G, orig_node, dest_node, weight="length")

    # Dijkstra or/and A*
    def shortest_path_dijkstra(self, origin, destination):
        nodes, edges = ox.graph_to_gdfs(self.osm_network())
        print(nodes.dtypes)
        print(nodes.iloc[1])

    def all_paths(self):
        pass
