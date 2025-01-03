import heapq
from map.map import Map
from utils.distance_between_coords import distance_between_coords

from typing import Literal

from utils.choose_best_routes_from_multiple_capitals import choose_best_routes_from_multiple_capitals 

def A_star(map: Map, end_city_id: str, groceries_tons: int):
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
    end_city = map.get_city_by_id(end_city_id)

    open_list = []
    heapq.heappush(open_list, (0, start_city["id"]))
    g_costs = {start_city["id"]: 0}
    parent = {start_city["id"]: None}
    closed_list = set()

    while open_list:
        _, current_city_id = heapq.heappop(open_list)
        current_city = map.get_city_by_id(current_city_id)

        if current_city_id == end_city_id:
            # Construct the route
            route = []
            while current_city_id is not None:
                route.append(current_city_id)
                current_city_id = parent[current_city_id]
            route.reverse()
            return route

        closed_list.add(current_city_id)

        for weather, neighbor_ids in current_city["neighbors"].items():
            if route_type == "land" and weather != "land":
                continue
            if route_type == "air" and weather != "air":
                continue
            if route_type == "sea" and weather != "sea":
                continue

            for neighbor_id in neighbor_ids:
                if neighbor_id in closed_list:
                    continue

                neighbor = map.get_city_by_id(neighbor_id)
                travel_cost = distance_between_coords(
                    current_city["map_coords"], neighbor["map_coords"]
                )
                tentative_g_cost = g_costs[current_city_id] + travel_cost

                if (
                    neighbor_id not in g_costs
                    or tentative_g_cost < g_costs[neighbor_id]
                ):
                    g_costs[neighbor_id] = tentative_g_cost
                    heuristic = distance_between_coords(
                        neighbor["map_coords"], end_city["map_coords"]
                    )
                    f_cost = tentative_g_cost + heuristic
                    heapq.heappush(open_list, (f_cost, neighbor_id))
                    parent[neighbor_id] = current_city_id

    return None  # Return None if no path is found


def create_route(map: Map, path: list, VehicleClass):
    route = []
    for i in range(len(path) - 1):
        current_city_id = path[i]
        next_city_id = path[i + 1]
        vehicle = VehicleClass(map, current_city_id, next_city_id)
        route.append(vehicle)
    return route
