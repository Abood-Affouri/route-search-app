import json
import math
import plotly.graph_objects as go


def load_map(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_uploaded_map(uploaded_file):
    return json.load(uploaded_file)


def build_graph(map_data):
    graph = {city["name"]: {} for city in map_data["cities"]}

    for road in map_data["roads"]:
        city_a = road["from"]
        city_b = road["to"]
        distance = road["km"]

        graph[city_a][city_b] = distance
        graph[city_b][city_a] = distance

    return graph


def get_coordinates(map_data):
    return {
        city["name"]: (city["x"], city["y"])
        for city in map_data["cities"]
    }


def validate_map(map_data):
    if "cities" not in map_data or "roads" not in map_data:
        raise ValueError("Map must contain cities and roads")

    city_names = set()

    for city in map_data["cities"]:
        if "name" not in city or "x" not in city or "y" not in city:
            raise ValueError("Each city must have a name, x, and y")

        if city["name"] in city_names:
            raise ValueError("City names must be unique")

        city_names.add(city["name"])

    for road in map_data["roads"]:
        if "from" not in road or "to" not in road or "km" not in road:
            raise ValueError("Each road must have from, to, and km")

        if road["from"] not in city_names or road["to"] not in city_names:
            raise ValueError("Each road must connect existing cities")

        if road["km"] <= 0:
            raise ValueError("Road distance must be positive")

    return True


def heuristic(coordinates, city, goal):
    x1, y1 = coordinates[city]
    x2, y2 = coordinates[goal]

    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return math.floor(distance)

def draw_map(map_data, path=None):
    coordinates = get_coordinates(map_data)
    figure = go.Figure()

    for road in map_data["roads"]:
        city_a = road["from"]
        city_b = road["to"]
        x1, y1 = coordinates[city_a]
        x2, y2 = coordinates[city_b]

        figure.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(color="gray", width=2),
            hoverinfo="text",
            text=f"{city_a} — {city_b}: {road['km']} km",
            showlegend=False
        ))

    city_names = [city["name"] for city in map_data["cities"]]
    city_x = [coordinates[name][0] for name in city_names]
    city_y = [coordinates[name][1] for name in city_names]

    figure.add_trace(go.Scatter(
        x=city_x,
        y=city_y,
        mode="markers+text",
        text=city_names,
        textposition="top center",
        marker=dict(size=12, color="#2563eb"),
        name="Cities"
    ))

    if path:
        for city_a, city_b in zip(path, path[1:]):
            x1, y1 = coordinates[city_a]
            x2, y2 = coordinates[city_b]

            figure.add_trace(go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color="red", width=5),
                showlegend=False
            ))

    figure.update_layout(
        title=map_data.get("name", "City Road Map"),
        xaxis_title="X (km)",
        yaxis_title="Y (km)",
        showlegend=False
    )
    figure.update_yaxes(scaleanchor="x", scaleratio=1)

    return figure