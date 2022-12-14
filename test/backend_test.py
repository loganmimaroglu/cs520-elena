import os, sys
import networkx as nx
sys.path.append('./')

from src.backend.model import map_model
from src.backend.view import path_finding_view
# from src import *
# orig_point = (42.39563733630018, -72.51070388052955)
# dest_point = (42.34096806753386, -72.51882985477177)

orig_point = (37.826250, -122.247604)
dest_point = (37.823049, -122.242448)

orig_address = "141 Echo Avenue, Oakland, CA 94611"
dest_address = "1123 Oakland Avenue, Piedmont, CA 94611"

m = map_model.MapModel("../data/piedmont.graphml")
p = path_finding_view.PathFindingView()
# path = p.get_route(m.osm_network(), orig_address, dest_address, grade="max", scale=1.1)
# print(path)


import unittest
  
class Test(unittest.TestCase):
    # test the shortest path function 
    def test_shortest_path(self):
        G = m.osm_network()
        path1 = [1,2,5]
        path2 = [1,8,5]
        G.add_nodes_from(path1)
        G.add_nodes_from(path2)
        G.add_edges_from([(1,2),(2,5)])
        G.add_edges_from([(1,8),(8,5)])
        G[1][2][0]["length"] = 1
        G[2][5][0]["length"] = 1
        G[1][8][0]["length"] = 10
        G[8][5][0]["length"] = 10

        dis, output = p.shortest_path_and_length(G, 1,5)
        true_path =  [1,2,5]
        true_dis = 2
        self.assertEqual(output, true_path)
        self.assertEqual(dis, true_dis)
        return 
  
if __name__ == '__main__':
    unittest.main()