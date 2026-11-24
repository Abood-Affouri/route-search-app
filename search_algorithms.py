from collections import deque
import heapq
import math

from map_utils import heuristic


def bfs(graph, coordinates, start, goal):
    frontier = deque([(start, [start])])
    discovered = {start}
    steps = 0

    while frontier:
        city, path = frontier.popleft()

        if city == goal:
            cost = sum(
                graph[path[index]][path[index + 1]]
                for index in range(len(path) - 1)
            )
            return {
                "path": path,
                "cost": cost,
                "steps": steps
            }

        steps += 1

        for neighbor in sorted(graph[city]):
            if neighbor not in discovered:
                discovered.add(neighbor)
                frontier.append((neighbor, path + [neighbor]))

    return {
        "path": None,
        "cost": None,
        "steps": steps
    }


def _result(path, cost, steps):
    return {"path": path, "cost": cost, "steps": steps}


def _invalid(graph, start, goal):
    return start not in graph or goal not in graph


def dfs(graph, coordinates, start, goal):
    if _invalid(graph, start, goal):
        return _result(None, None, 0)

    frontier = [(start, [start], 0)]
    explored = set()
    steps = 0

    while frontier:
        city, path, cost = frontier.pop()

        if city in explored:
            continue

        explored.add(city)

        if city == goal:
            return _result(path, cost, steps)

        steps += 1

        for neighbor in sorted(graph[city], reverse=True):
            if neighbor not in explored:
                frontier.append((neighbor, path + [neighbor], cost + graph[city][neighbor]))

    return _result(None, None, steps)


def ucs(graph, coordinates, start, goal):
    if _invalid(graph, start, goal):
        return _result(None, None, 0)

    frontier = [(0, start, [start])]
    explored = set()
    steps = 0

    while frontier:
        cost, city, path = heapq.heappop(frontier)

        if city in explored:
            continue

        explored.add(city)

        if city == goal:
            return _result(path, cost, steps)

        steps += 1

        for neighbor in sorted(graph[city]):
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + graph[city][neighbor], neighbor, path + [neighbor]))

    return _result(None, None, steps)


def astar(graph, coordinates, start, goal):
    if _invalid(graph, start, goal):
        return _result(None, None, 0)

    frontier = [(heuristic(coordinates, start, goal), start, 0, [start])]
    explored = set()
    steps = 0

    while frontier:
        f, city, cost, path = heapq.heappop(frontier)

        if city in explored:
            continue

        explored.add(city)

        if city == goal:
            return _result(path, cost, steps)

        steps += 1

        for neighbor in sorted(graph[city]):
            if neighbor not in explored:
                new_cost = cost + graph[city][neighbor]
                new_f = new_cost + heuristic(coordinates, neighbor, goal)
                heapq.heappush(frontier, (new_f, neighbor, new_cost, path + [neighbor]))

    return _result(None, None, steps)


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
