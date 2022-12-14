import os, sys
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

path = p.get_route(m.osm_network(), orig_address, dest_address, grade="max", scale=1.1)
print(path)
