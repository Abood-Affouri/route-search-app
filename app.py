
import streamlit as st
from pathlib import Path
from comparison import compare_all
from search_algorithms import bfs, dfs, ucs, greedy, astar
from map_utils import (
    load_map,
    load_uploaded_map,
    validate_map,
    build_graph,
    get_coordinates,
    draw_map
)

st.set_page_config(
    page_title="West Bank Search",
    layout="wide"
)

st.title("West Bank Route Finder")

uploaded_file = st.sidebar.file_uploader(
    "Upload Custom Map",
    type=["json"]
)

try:
    if uploaded_file is not None:
        map_data = load_uploaded_map(uploaded_file)
    else:
        map_data = load_map(
            Path(__file__).parent / "westbank_map.json"
        )

    validate_map(map_data)

    graph = build_graph(map_data)
    coordinates = get_coordinates(map_data)

    if not graph:
        raise ValueError("The map contains no cities.")

except Exception as e:
    st.error(f"Invalid map: {e}")
    st.stop()

cities = sorted(graph)

left, right = st.columns(2)

start = left.selectbox("Start City", cities)

goal = right.selectbox(
    "Goal City",
    cities,
    index=len(cities) - 1
)

algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar
}

choice = st.selectbox(
    "Search Algorithm",
    list(algorithms) + ["Compare All"]
)

if st.button("Search", type="primary"):

    if choice == "Compare All":

        results, optimal = compare_all(
            graph,
            coordinates,
            start,
            goal,
            algorithms
        )

        rows = []

        for name, result in results.items():

            rows.append({
                "Algorithm": name,
                "Path": " → ".join(result["path"])
                if result["path"] is not None
                else "ما في طريق",
                "Cost (km)": result["cost"],
                "Steps": result["steps"],
                "Optimal": "Yes" if name in optimal else "No"
            })

        st.subheader("Algorithm Comparison")

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

        if optimal:
            st.success(
                "Lowest-cost algorithm(s): "
                + ", ".join(optimal)
            )
        else:
            st.warning("ما في طريق")

        tabs = st.tabs(list(results))

        for tab, (name, result) in zip(
            tabs, results.items()
        ):
            with tab:

                st.subheader(name)

                if result["path"] is None:
                    st.warning("ما في طريق")

                else:
                    st.success(
                        " → ".join(result["path"])
                    )

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Total Cost (km)",
                        result["cost"]
                    )

                    col2.metric(
                        "Steps",
                        result["steps"]
                    )

                st.plotly_chart(
                    draw_map(map_data, result["path"]),
                    use_container_width=True,
                    key=f"map_{name}"
                )

    else:

        result = algorithms[choice](
            graph,
            coordinates,
            start,
            goal
        )

        if result["path"] is None:

            st.warning("ما في طريق")

            st.plotly_chart(
                draw_map(map_data),
                use_container_width=True
            )

        else:

            st.success(
                " → ".join(result["path"])
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Cost (km)",
                result["cost"]
            )

            col2.metric(
                "Steps",
                result["steps"]
            )

            st.plotly_chart(
                draw_map(map_data, result["path"]),
                use_container_width=True
            )

else:

    st.plotly_chart(
        draw_map(map_data),
        use_container_width=True
    )
