import math
from map.map import Map
from utils.distance_between_coords import distance_between_coords
from typing import Literal
from utils.choose_best_routes_from_multiple_capitals import (
    choose_best_routes_from_multiple_capitals,
)

def iddfs(map: Map, end_city_id: str, groceries_tons: int, max_depth: int = 1000):
    end_city_id = str(end_city_id)
    end_city = map.get_city_by_id(end_city_id)
    capitals = map.get_capitals()
    nearest_capitals = sorted(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )

    multiple_routes = choose_best_routes_from_multiple_capitals(
        map,
        nearest_capitals,
        end_city_id,
        groceries_tons,
        lambda m, start_id, end_id, route_type: find_path_with_iddfs(
            m, start_id, end_id, route_type, max_depth
        )
    )

    flattened_routes = [
        vehicle for route_info in multiple_routes for vehicle in route_info["route"]
    ]
    return flattened_routes


def find_path_with_iddfs(
    map: Map,
    start_city_id: str,
    end_city_id: str,
    route_type: Literal["land", "air", "sea"] = "land",
    max_depth: int = 1000,
):
    for depth in range(max_depth + 1):
        result = dls(map, start_city_id, end_city_id, route_type, depth)
        if result is not None:
            return result
    print(f"No path found within the max depth of {max_depth}.")
    return None


def dls(
    map: Map,
    current_city_id: str,
    end_city_id: str,
    route_type: Literal["land", "air", "sea"] = "land",
    depth: int = 1000,
):
    stack = [current_city_id]
    visited = set()
    parent = {current_city_id: None}

    while stack:
        current_city_id = stack.pop()

        if current_city_id in visited:
            continue

        visited.add(current_city_id)

        if current_city_id == end_city_id:
            
            path = []
            while current_city_id is not None:
                path.append(current_city_id)
                current_city_id = parent[current_city_id]
            path.reverse()
            return path

        current_city = map.get_city_by_id(current_city_id)

        if depth > 0:
            for neighbor_id in current_city["neighbors"][route_type]:
                if neighbor_id not in visited:
                    stack.append(neighbor_id)
                    parent[neighbor_id] = current_city_id

    return None
