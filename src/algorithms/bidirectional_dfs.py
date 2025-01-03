from map.map import Map
from utils.distance_between_coords import distance_between_coords

from typing import Literal

from utils.choose_best_routes_from_multiple_capitals import choose_best_routes_from_multiple_capitals 


def bidirectional_dfs(map: Map, end_city_id: str, groceries_tons: int):
    end_city_id = str(end_city_id)
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capitals = sorted(
        capitals,
        key=lambda capital: distance_between_coords(capital["map_coords"], end_city["map_coords"]),
    )

    multiple_routes = choose_best_routes_from_multiple_capitals(map, nearest_capitals, end_city_id, groceries_tons, find_bidirectional_path)

    flattened_routes = [vehicle for route_info in multiple_routes for vehicle in route_info["route"]]
    return flattened_routes


def find_bidirectional_path(map: Map, start_city_id: str, end_city_id: str, route_type: Literal["land", "air", "sea"] = "land"):
    start_city = map.get_city_by_id(start_city_id)
    end_city = map.get_city_by_id(end_city_id)

    src_stack = [start_city]
    dest_stack = [end_city]
    src_visited = {start_city["id"]: None}
    dest_visited = {end_city["id"]: None}

    while src_stack and dest_stack:

        if src_stack:
            current_city = src_stack.pop()
            current_city_id = current_city["id"]

            if current_city_id in dest_visited:
                return reconstruct_bidirectional_path(
                    src_visited, dest_visited, current_city_id
                )

            for neighbor_id in current_city["neighbors"][route_type]:
                if neighbor_id not in src_visited:
                    src_stack.append(map.get_city_by_id(neighbor_id))
                    src_visited[neighbor_id] = current_city_id

        if dest_stack:
            current_city = dest_stack.pop()
            current_city_id = current_city["id"]

            if current_city_id in src_visited:

                return reconstruct_bidirectional_path(
                    src_visited, dest_visited, current_city_id
                )

            for neighbor_id in current_city["neighbors"][route_type]:
                if neighbor_id not in dest_visited:
                    dest_stack.append(map.get_city_by_id(neighbor_id))
                    dest_visited[neighbor_id] = current_city_id

    return None


def reconstruct_bidirectional_path(src_visited, dest_visited, meeting_point):
    path = []

    current_city_id = meeting_point
    while current_city_id is not None:
        path.append(current_city_id)
        current_city_id = src_visited[current_city_id]
    path.reverse()

    current_city_id = dest_visited[meeting_point]
    while current_city_id is not None:
        path.append(current_city_id)
        current_city_id = dest_visited[current_city_id]

    print(f"\nPath: {path}")
    return path
