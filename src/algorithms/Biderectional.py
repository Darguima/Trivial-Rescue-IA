import math
from collections import deque

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat


def bidirectional_bfs(map: Map, end_city_id: str, groceries_tons: int):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )
    start_city = nearest_capital

    src_queue = deque([start_city])
    src_visited = {start_city["id"]: None}
    dest_queue = deque([end_city])
    dest_visited = {end_city["id"]: None}

    while src_queue and dest_queue:
        if src_queue:
            current_city = src_queue.popleft()
            current_city_id = current_city["id"]

            for neighbor_id in current_city["neighbors"]["land"]:
                if neighbor_id not in src_visited:
                    src_queue.append(map.get_city_by_id(neighbor_id))
                    src_visited[neighbor_id] = current_city_id

                if neighbor_id in dest_visited:
                    return reconstruct_bidirectional_path(src_visited, dest_visited, neighbor_id)

        if dest_queue:
            current_city = dest_queue.popleft()
            current_city_id = current_city["id"]

            for neighbor_id in current_city["neighbors"]["land"]:
                if neighbor_id not in dest_visited:
                    dest_queue.append(map.get_city_by_id(neighbor_id))
                    dest_visited[neighbor_id] = current_city_id

                if neighbor_id in src_visited:
                    return reconstruct_bidirectional_path(src_visited, dest_visited, neighbor_id)

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

    return path

