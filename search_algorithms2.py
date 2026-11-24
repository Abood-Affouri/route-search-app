import heapq
import math


def heuristic(coordinates, city, goal):
    """Floor of great-circle distance in km; replace with team's heuristic if different."""
    lat1, lon1 = coordinates[city]
    lat2, lon2 = coordinates[goal]
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return math.floor(6371 * 2 * math.asin(min(1, math.sqrt(a))))


def greedy(graph, coordinates, start, goal):
    """Greedy Best-First Search. Steps = unique expanded nodes, including goal.

    Tie-break: (heuristic, city name). Graph: {city: {neighbor: edge_cost}}.
    """
    if start not in graph or goal not in graph:
        return {"path": None, "cost": None, "steps": 0}
    if start not in coordinates or goal not in coordinates:
        raise ValueError("Missing coordinates for start or goal")
    frontier = [(heuristic(coordinates, start, goal), start, [start], 0)]
    visited = set()
    steps = 0
    while frontier:
        _, city, path, cost = heapq.heappop(frontier)
        if city in visited:
            continue
        visited.add(city)
        steps += 1
        if city == goal:
            return {"path": path, "cost": cost, "steps": steps}
        for neighbor in sorted(graph[city]):
            if neighbor not in visited:
                if neighbor not in coordinates:
                    raise ValueError(f"Missing coordinates for {neighbor}")
                heapq.heappush(frontier, (
                    heuristic(coordinates, neighbor, goal),
                    neighbor,
                    path + [neighbor],
                    cost + graph[city][neighbor],
                ))
    return {"path": None, "cost": None, "steps": steps}
