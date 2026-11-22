from map_utils import load_map, validate_map, build_graph
from search_algorithms import bfs

map_data = load_map("westbank_map.json")
validate_map(map_data)
graph = build_graph(map_data)

result = bfs(graph, "Jenin", "Hebron")

print("Path:", result["path"])
print("Cost:", result["cost"])
print("Steps:", result["steps"])