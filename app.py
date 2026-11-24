import streamlit as st
from comparison import compare_all
from search_algorithms import greedy
import search_algorithms as search

try:
    from sample_data import graph, coordinates
except ImportError:
    graph, coordinates = None, None

st.set_page_config(page_title="West Bank Search", layout="wide")
st.title("West Bank Route Finder")
if graph is None or coordinates is None:
    st.warning("Connect the team map_utils and westbank_map.json before running searches.")
    st.stop()

cities = sorted(graph)
left, right = st.columns(2)
start = left.selectbox("Start city", cities)
goal = right.selectbox("Goal city", cities, index=len(cities)-1)

algorithms = {label: getattr(search, name) for label, name in [("BFS", "bfs"), ("DFS", "dfs"), ("UCS", "ucs"), ("Greedy", "greedy"), ("A*", "astar")] if callable(getattr(search, name, None))}
choice = st.selectbox("Algorithm", list(algorithms) + ["Compare All"])

if st.button("Search", type="primary"):
    if choice == "Compare All":
        results, optimal = compare_all(graph, coordinates, start, goal, algorithms)
        rows = []
        for name, result in results.items():
            rows.append({
                "Algorithm": name,
                "Path": " → ".join(result["path"]) if result["path"] is not None else "ما في طريق",
                "Cost": result["cost"],
                "Steps": result["steps"],
                "Optimal": "Yes" if name in optimal else "No",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
        if optimal:
            st.success("Lowest-cost result(s): " + ", ".join(optimal))
        else:
            st.warning("ما في طريق")
    else:
        result = algorithms[choice](graph, coordinates, start, goal)
        if result["path"] is None:
            st.warning("ما في طريق")
        else:
            st.success(" → ".join(result["path"]))
            col1, col2 = st.columns(2)
            col1.metric("Cost", result["cost"])
            col2.metric("Steps", result["steps"])
