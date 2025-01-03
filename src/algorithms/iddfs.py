import math

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from typing import Literal

from utils.choose_best_routes_from_multiple_capitals import choose_best_routes_from_multiple_capitals 

def iddfs(map: Map, end_city_id: str, groceries_tons: int):
    end_city_id = str(end_city_id)
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capitals = sorted(
        capitals,
        key=lambda capital: distance_between_coords(capital["map_coords"], end_city["map_coords"]),
    )

    multiple_routes = choose_best_routes_from_multiple_capitals(map, nearest_capitals, end_city_id, groceries_tons, find_path)

    flattened_routes = [vehicle for route_info in multiple_routes for vehicle in route_info["route"]]
    return flattened_routes


def find_path(map: Map, start_city_id: str, end_city_id: str, route_type: Literal["land", "air", "sea"] = "land"):
    start_city = map.get_city_by_id(start_city_id)

    depth = 0
    while True:
        result = dls(map, start_city["id"], end_city_id, depth, route_type)
        if result is not None:
            return result
        depth += 1


def dls(map: Map, current_city_id: str, end_city_id: str, depth: int, route_type: Literal["land", "air", "sea"] = "land"):
    if depth == 0:
        return None
    stack = [(current_city_id, 0)]
    visited = set()
    parent = {current_city_id: None}

    while stack:
        current_city_id, current_depth = stack.pop()

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

        if current_depth < depth:
            current_city = map.get_city_by_id(current_city_id)
            for neighbor_id in current_city["neighbors"][route_type]:
                if neighbor_id not in visited:
                    stack.append((neighbor_id, current_depth + 1))
                    parent[neighbor_id] = current_city_id

    return None
