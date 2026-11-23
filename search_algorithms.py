from collections import deque


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