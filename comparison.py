from search_algorithms import greedy


def compare_all(graph, coordinates, start, goal, algorithms=None):
    """Returns (results, optimal_names); skips missing paths for optimal calculation.

    Pass all five functions in algorithms once teammates' functions are available.
    """
    if algorithms is None:
        algorithms = {"Greedy": greedy}
    results = {
        name: function(graph, coordinates, start, goal)
        for name, function in algorithms.items()
    }
    return results, find_optimal(results)


def find_optimal(results):
    valid = {name: result for name, result in results.items()
             if result.get("path") is not None and result.get("cost") is not None}
    if not valid:
        return []
    minimum = min(result["cost"] for result in valid.values())
    optimal = [name for name, result in valid.items() if math_isclose(result["cost"], minimum)]
    return optimal


def math_isclose(a, b):
    import math
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-9)
