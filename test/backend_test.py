import os, sys
import osmnx as ox
import networkx as nx
import unittest
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

# m = map_model.MapModel("../data/piedmont.graphml")
# p = path_finding_view.PathFindingView()
# path = p.get_route(m.osm_network(), orig_address, dest_address, grade="max", scale=1.1)
# print(path)

  
class TestPathFinding(unittest.TestCase):
    global m 
    global p
    m = map_model.MapModel("../data/piedmont.graphml")
    p = p = path_finding_view.PathFindingView()

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
        true_path =  path1
        true_dis = 2
        self.assertEqual(output, true_path)
        self.assertEqual(dis, true_dis)

    #test when the graph has more paths
    def test_shortest_path2(self):
        G = m.osm_network()
        path1 = [1,2,3,4,5]
        path2 = [1,2,7,10,5]
        path3 = [1,21,53,5]
        G.add_nodes_from(path1)
        G.add_nodes_from(path2)
        G.add_nodes_from(path3)

        G.add_edges_from([(1,2),(2,3),(3,4),(4,5)])
        G.add_edges_from([(1,2),(2,7),(7,10),(10,5)])
        G.add_edges_from([(1,21),(21,53), (53,5)])

        G[1][2][0]["length"] = 1
        G[2][3][0]["length"] = 3
        G[3][4][0]["length"] = 4
        G[4][5][0]["length"] = 10

        G[1][2][0]["length"] = 1
        G[2][7][0]["length"] = 12
        G[7][10][0]["length"] = 1
        G[10][5][0]["length"] = 2

        G[1][21][0]["length"] = 10
        G[21][53][0]["length"] = 10
        G[53][5][0]["length"] = 100

        dis, output = p.shortest_path_and_length(G, 1,5)
        true_path =  path2
        true_dis = 16
        self.assertEqual(output, true_path)
        self.assertEqual(dis, true_dis)

    #test the return shortest path has the maximum array size \\
    #while all the paths have the same distance
    def test_shortest_path3(self):
        G = m.osm_network()
        path1 = [1,2,3,4,5]
        path2 = [1,2,7,10,520,5]
        path3 = [1,21,53,5] 

        G.add_nodes_from(path1)
        G.add_nodes_from(path2)
        G.add_nodes_from(path3)

        G.add_edges_from([(1,2),(2,3),(3,4),(4,5)])
        G.add_edges_from([(1,2),(2,7),(7,10),(10,520), (520,5)])
        G.add_edges_from([(1,21),(21,53), (53,5)])

        G[1][2][0]["length"] = 1
        G[2][3][0]["length"] = 1
        G[3][4][0]["length"] = 1
        G[4][5][0]["length"] = 2

        G[1][2][0]["length"] = 1
        G[2][7][0]["length"] = 1
        G[7][10][0]["length"] = 1
        G[10][520][0]["length"] = 1
        G[520][5][0]["length"] = 1

        G[1][21][0]["length"] = 1
        G[21][53][0]["length"] = 1
        G[53][5][0]["length"] = 3

        dis, output = p.shortest_path_and_length(G, 1,5)
        true_path =  path2
        true_dis = 5

        self.assertEqual(output, true_path)
        self.assertEqual(dis, true_dis)
    
    #test the filter path function
    def test_filter_path(self):
        G = m.osm_network()
        path1 = [1,2,10,3]
        path2 = [1,4,11,3]
        path3 = [1,5,12,3] 

        G.add_nodes_from(path1)
        G.add_nodes_from(path2)
        G.add_nodes_from(path3)

        G.add_edges_from([(1,2),(2,10),(10,3)])
        G.add_edges_from([(1,4),(4,11),(11,3)])
        G.add_edges_from([(1,5),(5,12),(12,3)])

        G[1][2][0]["length"] = 3
        G[2][10][0]["length"] = 3
        G[10][3][0]["length"] = 3

        G[1][4][0]["length"] = 4
        G[4][11][0]["length"] = 5
        G[11][3][0]["length"] = 4

        G[1][5][0]["length"] = 2
        G[5][12][0]["length"] = 3
        G[12][3][0]["length"] = 7

        G.nodes[1]['x'] = 0.51515
        G.nodes[1]['y'] = 0.605

        G.nodes[2]['x'] = 2.1564
        G.nodes[2]['y'] = 34.154

        G.nodes[3]['x'] = 0.605
        G.nodes[3]['y'] = 0.11145

        G.nodes[4]['x'] = 3.878
        G.nodes[4]['y'] = 0.4851

        G.nodes[5]['x'] = 7.154
        G.nodes[5]['y'] = 8.848

        G.nodes[10]['x'] = 14.05
        G.nodes[10]['y'] = 13.005

        G.nodes[11]['x'] = 102.11
        G.nodes[11]['y'] = 74.15

        G.nodes[12]['x'] = 90.15
        G.nodes[12]['y'] = 88.51
        true_paths =  [path1,path2,path3]
        output = p.simple_paths_filtered(G, 1,3, scale=1.5)
        self.assertEqual(output, true_paths)

        true_paths = [path1]
        output = p.simple_paths_filtered(G, 1,3, scale=1.0)
        self.assertEqual(output, true_paths)

        true_paths = [path1,path3]
        output = p.simple_paths_filtered(G, 1,3, scale=1.4)
        self.assertEqual(output, true_paths)

    #test input validation for the scale 
    def test_scale(self):
        G = m.osm_network()
        self.assertRaises(TypeError, p.get_route,G,1,2,'max', 0.5)
        self.assertRaises(TypeError, p.get_route,G,1,2,'max', -0.5)


# class includes test cases for the get route methods, maximum and minimum and neither. 
class TestGetRoute(unittest.TestCase):
    global m 
    global p
    global G
    global path1
    global path2
    global path3
    m = map_model.MapModel("../data/piedmont.graphml")
    p = p = path_finding_view.PathFindingView()
    G = m.osm_network()
    path1 = [1,2,10,3]
    path2 = [1,4,11,3]
    path3 = [1,5,12,3] 

    G.add_nodes_from(path1)
    G.add_nodes_from(path2)
    G.add_nodes_from(path3)

    G.add_edges_from([(1,2), (2,10), (10,3)])
    G.add_edges_from([(1,4),(4,11),(11,3)])
    G.add_edges_from([(1,5),(5,12),(12,3)])

    G.nodes[1]['x'] = -122.247795
    G.nodes[1]['y'] = 37.826389
    
    G.nodes[2]['x'] = 2.1564
    G.nodes[2]['y'] = 34.154

    G.nodes[4]['x'] = 3.878
    G.nodes[4]['y'] = 0.4851

    G.nodes[5]['x'] = 7.154
    G.nodes[5]['y'] = 8.848

    G.nodes[10]['x'] = 14.05
    G.nodes[10]['y'] = 13.005

    G.nodes[11]['x'] = 102.11
    G.nodes[11]['y'] = 74.15

    G.nodes[12]['x'] = 90.15
    G.nodes[12]['y'] = 88.51

    G.nodes[3]['x'] = -122.248543
    G.nodes[3]['y'] = 37.827395

    G[1][2][0]["length"] = 3
    G[2][10][0]["length"] = 3
    G[10][3][0]["length"] = 3

    G[1][2][0]["grade_abs"] = 0.8159
    G[2][10][0]["grade_abs"] = 0.2005
    G[10][3][0]["grade_abs"] = 0.1145

    G[1][4][0]["length"] = 4
    G[4][11][0]["length"] = 5
    G[11][3][0]["length"] = 4


    G[1][4][0]["grade_abs"] = 0.6648
    G[4][11][0]["grade_abs"] = 0.0001
    G[11][3][0]["grade_abs"] = 0.0002

    G[1][5][0]["length"] = 2
    G[5][12][0]["length"] = 3
    G[12][3][0]["length"] = 7

    G[1][5][0]["grade_abs"] = 0.4951
    G[5][12][0]["grade_abs"] = 0.2618
    G[12][3][0]["grade_abs"] = 0.5204

    #test maximum, the maximum elevation path is path 3
    def test_get_route_max(self):
        output = p.get_route(G,orig = "141 Echo Avenue, Oakland, CA 94611", dest = "81 Echo Avenue, Oakland, CA 94611", grade='max', scale=1.5)
        true_path = [[G.nodes[id]['x'], G.nodes[id]['y']] for id in path3]
        self.assertEqual(output, true_path)

    #test minimum, the minimum elevation path is path 2
    def test_get_route_min(self):
        output = p.get_route(G,orig = "141 Echo Avenue, Oakland, CA 94611", dest = "81 Echo Avenue, Oakland, CA 94611", grade='min', scale=1.5)
        true_path = [[G.nodes[id]['x'], G.nodes[id]['y']] for id in path2]
        self.assertEqual(output, true_path)

    #test grade is none, it should return the closest path to the scaled path or the shortest path if scale is None
    def test_get_route(self):
        output = p.get_route(G,orig = "141 Echo Avenue, Oakland, CA 94611", dest = "81 Echo Avenue, Oakland, CA 94611", grade=None, scale=1.5)
        true_path = [[G.nodes[id]['x'], G.nodes[id]['y']] for id in path2]
        self.assertEqual(output, true_path)

    #test with a different scale
    def test_get_route2(self):
        output = p.get_route(G,orig = "141 Echo Avenue, Oakland, CA 94611", dest = "81 Echo Avenue, Oakland, CA 94611", grade=None, scale=1.4)
        true_path = [[G.nodes[id]['x'], G.nodes[id]['y']] for id in path3]
        self.assertEqual(output, true_path)
    
    #test when scale is none, it should just return the shorest path
    def test_get_route3(self):
        output = p.get_route(G,orig = "141 Echo Avenue, Oakland, CA 94611", dest = "81 Echo Avenue, Oakland, CA 94611", grade=None, scale=None)
        true_path = [[G.nodes[id]['x'], G.nodes[id]['y']] for id in path1]
        self.assertEqual(output, true_path)
if __name__ == '__main__':
    unittest.main()