from src.backend.model import map_model
from src.backend.view import path_finding_view

# orig_point = (42.39563733630018, -72.51070388052955)
# dest_point = (42.34096806753386, -72.51882985477177)

orig_point = (37.826250, -122.247604)
dest_point = (37.823049, -122.242448)

m = map_model.MapModel()
p = path_finding_view.PathFindingView()

orig_node, dest_node = p.gps_to_nodes(m.osm_network(), orig_point, dest_point)

path = p.get_route(m.osm_network(), orig_node, dest_node, grade="max", scale=1.1)
print(path)
