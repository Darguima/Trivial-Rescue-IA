from map.map import Map
from utils.distance_between_coords import distance_between_coords

from typing import Literal

from utils.choose_best_routes_from_multiple_capitals import choose_best_routes_from_multiple_capitals 
from utils.print_utils import input_centered


def depth_limited_search(map: Map, end_city_id: str, groceries_tons: int):
    limit = int(input_centered("Limit: "))

    def find_path_with_limit(map: Map, start_city_id: str, end_city_id: str, route_type: Literal["land", "air", "sea"] = "land"):
        find_path(map, start_city_id, end_city_id, limit, route_type)

    end_city_id = str(end_city_id)
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capitals = sorted(
        capitals,
        key=lambda capital: distance_between_coords(capital["map_coords"], end_city["map_coords"]),
    )

    multiple_routes = choose_best_routes_from_multiple_capitals(map, nearest_capitals, end_city_id, groceries_tons, find_path_with_limit)

    flattened_routes = [vehicle for route_info in multiple_routes for vehicle in route_info["route"]]
    return flattened_routes


def find_path(map: Map, start_city_id: str, end_city_id: str, limit, route_type: Literal["land", "air", "sea"] = "land"):
    start_city = map.get_city_by_id(start_city_id)
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )
    start_city = nearest_capital

    stack = [(start_city, 0)]
    visited = set()
    parent = {start_city["id"]: None}

    while stack:
        current_city, depth = stack.pop()
        current_city_id = current_city["id"]

        if current_city_id in visited:
            continue

        visited.add(current_city_id)

        if current_city_id == end_city_id:
            # Reconstruct the path from start_city to end_city
            path = []
            while current_city_id is not None:
                path.append(current_city_id)
                current_city_id = parent[current_city_id]
            path.reverse()

            return path

        if depth < limit:
            for neighbor_id in current_city["neighbors"][route_type]:
                if neighbor_id not in visited:
                    stack.append((map.get_city_by_id(neighbor_id), depth + 1))
                    parent[neighbor_id] = current_city_id

    return None
