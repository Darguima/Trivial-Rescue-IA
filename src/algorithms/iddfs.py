import math

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter


def iddfs(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path(map, end_city_id)

    if path is None:
        print("\nPath not found")
        return None

    print("\nPath found:", path)

    car_route = [Car(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    truck_route = [Truck(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    helicopter_route = [Helicopter(map, path[0], path[-1])]

    # Verificar se o número de veículos necessário existe na capital que foi escolhida
    start_city_id = path[0]
    capital_info = map.get_city_by_id(start_city_id)["capital_info"]
    cars_qnt_needed = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
    trucks_qnt_needed = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
    helicopters_qnt_needed = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)

    if capital_info["cars"] < cars_qnt_needed:
        car_cost = None
    else:
        car_cost = sum_vehicles_cost(car_route, [cars_qnt_needed] * len(car_route))

    if capital_info["trucks"] < trucks_qnt_needed:
        truck_cost = None
    else:
        truck_cost = sum_vehicles_cost(
            truck_route, [trucks_qnt_needed] * len(truck_route)
        )

    if capital_info["helicopters"] < helicopters_qnt_needed:
        helicopter_cost = None
    else:
        helicopter_cost = sum_vehicles_cost(
            helicopter_route, [helicopters_qnt_needed] * len(helicopter_route)
        )

    print("\nRoute costs for each vehicle: (None is not possible routes)")
    print("\nCar cost of the path:", car_cost)
    print("Truck cost of the path:", truck_cost)
    print("Helicopter cost of the path:", helicopter_cost)

    options = [
        (car_cost, cars_qnt_needed, car_route),
        (truck_cost, trucks_qnt_needed, truck_route),
        (helicopter_cost, helicopters_qnt_needed, helicopter_route),
    ]
    options = [option for option in options if option[0] is not None]

    best_index, best_cost = min(
        enumerate(options),
        key=lambda option: option[1][0].get_final_cost() * option[1][1],
    )

    print(f"\nBest route:")
    print("\tindex:", best_index)
    print("\tfinal cost:", best_cost[0].get_final_cost())
    print("\tvehicles needed:", best_cost[1])
    print("\t1 vehicle cost:", best_cost[0].get_final_cost())

    return options[best_index][2]


def find_path(map: Map, end_city_id: str):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )
    start_city = nearest_capital

    depth = 0
    while True:
        result = dls(map, start_city["id"], end_city_id, depth)
        if result is not None:
            return result
        depth += 1


def dls(map: Map, current_city_id: str, end_city_id: str, depth: int):
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
            for neighbor_id in current_city["neighbors"]["land"]:
                if neighbor_id not in visited:
                    stack.append((neighbor_id, current_depth + 1))
                    parent[neighbor_id] = current_city_id

    return None
