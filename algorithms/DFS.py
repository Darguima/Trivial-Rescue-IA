from map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter

def depth_first_search(map: Map, end_city_id: str):
    path = find_path(map, end_city_id)
    print("\nPath found:", path)

    car_route = [Car(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    truck_route = [Truck(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    helicopter_route = [Helicopter(map, path[0], path[-1])]

    print("\nCar cost of the path:", sum_vehicles_cost(car_route))
    print("Truck cost of the path:", sum_vehicles_cost(truck_route))
    print("Helicopter cost of the path:", sum_vehicles_cost(helicopter_route))

def find_path(map: Map, end_city_id: str):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(capitals, key=lambda capital: distance_between_coords(capital["map_coords"], end_city["map_coords"]))
    start_city = nearest_capital

    stack = [start_city]
    visited = set()
    parent = {start_city["id"]: None}

    while stack:
        current_city = stack.pop()
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

        for neighbor_id in current_city["neighbors"]["land"]:
          neighbor_id = str(neighbor_id)
          if neighbor_id not in visited:
            stack.append(map.get_city_by_id(neighbor_id))
            parent[neighbor_id] = current_city_id

    return None

