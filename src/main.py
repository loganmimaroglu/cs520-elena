import model

# orig_point = (42.39563733630018, -72.51070388052955)
# dest_point = (42.34096806753386, -72.51882985477177)

orig_point = (37.826250, -122.247604)

dest_point = (37.823049, -122.242448)

m = model.Model()
m.osm_network()
# print(m.shortest_path_and_length(orig_point, dest_point))
l, p = m.shortest_path_and_length(orig_point, dest_point)
print('shortest path:',p)
print('alternative path with maximizing elevation gain:',m.maximize_elevation_path(orig_point, dest_point, 1.1))
# x_percent = 1.2
# paths = m.all_paths(orig_point, dest_point, x_percent)

# print(list(paths))
