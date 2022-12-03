import model

orig_point = (42.39563733630018, -72.51070388052955)
dest_point = (42.34096806753386, -72.51882985477177)

m = model.Model()
m.shortest_path_dijkstra(orig_point, dest_point)
