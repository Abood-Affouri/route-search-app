from map_utils import load_map, build_graph, get_coordinates, validate_map, heuristic, draw_map

map_data = load_map("westbank_map.json")
validate_map(map_data)

graph = build_graph(map_data)
coordinates = get_coordinates(map_data)

print("Number of cities:", len(graph))
print("Jenin neighbors:", graph["Jenin"])
print("Jenin coordinates:", coordinates["Jenin"])
print("Distance estimate from Jenin to Hebron:", heuristic(coordinates, "Jenin", "Hebron"))

figure = draw_map(map_data)
figure.show()