import osmnx as ox
import networkx as nx
import os
from dotenv import load_dotenv
import math
import numpy as np


class MapModel(object):
    def __init__(self):
        self.filepath = "./data/piedmont.graphml"
        self.route_map = self.osm_network()

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

        g = ox.graph_from_place("Piedmont, California, USA", network_type="drive")

        try:
            load_dotenv()

            google_elevation_api_key = os.getenv('google_elevation_api_key')

            g = ox.add_node_elevations_google(g, api_key=google_elevation_api_key)
            g = ox.add_edge_grades(g, add_absolute=True)

            ox.save_graphml(g, self.filepath)

        except ImportError:
            print("You need a google_elevation_api_key in your .env to run this.")

        return g
