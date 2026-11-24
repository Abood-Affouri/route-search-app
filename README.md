# West Bank Route Finder — Mohammad's Independent Module

Personal contribution: **Greedy Best-First Search**, Streamlit interface, and `Compare All` framework. Team integration is required before running the full application.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Interface contract

All five algorithms should accept `(graph, coordinates, start, goal)` and return:

```python
{"path": ["Jenin", "Nablus"], "cost": 42, "steps": 2}
```

For unreachable destinations: `{"path": None, "cost": None, "steps": N}`.

`graph` is assumed to be `{city: {neighbor: road_cost}}`, and `coordinates` is `{city: (latitude, longitude)}`.

Greedy uses a min-heap ordered by `(floor(haversine_distance_km), city_name)`; neighbors are iterated alphabetically. `steps` counts unique expanded nodes, including the goal. Confirm these conventions against the assignment and teammates' A* implementation.

## Compare All

`compare_all` accepts an optional mapping of algorithm names to callables. It ignores `path=None` when finding the minimum cost and allows multiple names to tie. The UI automatically registers available functions with the agreed names; merge BFS, DFS, UCS, and A* into the shared module. `find_optimal(results)` returns all lowest-cost successful algorithm names.

Example after merging:

```python
from search_algorithms import bfs, dfs, ucs, greedy, astar
algorithms = {"BFS": bfs, "DFS": dfs, "UCS": ucs, "Greedy": greedy, "A*": astar}
```

## Integration pending

- Replace sample data with the actual `westbank_map.json` and `map_utils.py` outputs.
- Confirm the graph and coordinates formats.
- Confirm heuristic formula, tie-breaking, and `steps` definition.
- Connect the team's map rendering and file upload to Streamlit.

No sample data is included in this personal submission. The app stops with a message until the team map is connected (or optional local sample_data is provided).
