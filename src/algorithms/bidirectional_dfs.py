import math
from collections import deque
from map.map import Map
from utils.distance_between_coords import distance_between_coords
from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat


def bidirectional_dfs(map: Map, end_city_id: str, groceries_tons: int):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )
    start_city = nearest_capital

    path = find_bidirectional_path(map, start_city, end_city)
    if path is None:
        print("\nPath not found")
        return None

    print("\nPath found:", path)

    car_route = [Car(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    truck_route = [Truck(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    helicopter_route = [Helicopter(map, path[0], path[-1])]

    capital_id = path[0]
    capital_info = map.get_city_by_id(capital_id)["capital_info"]

    cars_qnt_needed = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
    trucks_qnt_needed = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
    helicopters_qnt_needed = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)

    if capital_info["cars"] < cars_qnt_needed:
        car_cost = None
    else:
        car_cost = sum_vehicles_cost(car_route)

    if capital_info["trucks"] < trucks_qnt_needed:
        truck_cost = None
    else:
        truck_cost = sum_vehicles_cost(truck_route)

    if capital_info["helicopters"] < helicopters_qnt_needed:
        helicopter_cost = None
    else:
        helicopter_cost = sum_vehicles_cost(helicopter_route)

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

    if not options:
        print("\nNo valid routes available with the required vehicles.")
        return None

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


def find_bidirectional_path(map: Map, start_city, end_city):
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

            for neighbor_id in current_city["neighbors"]["land"]:
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

            for neighbor_id in current_city["neighbors"]["land"]:
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
