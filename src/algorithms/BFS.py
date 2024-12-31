import math

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter

def breadth_first_search(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path_bfs(map, end_city_id)

    if path is None:
        print("\nPath not found")
        return None

    print("\nPath found:", path)

    car_route = [Car(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    truck_route = [Truck(map, path[i], path[i + 1]) for i in range(len(path) - 1)]
    helicopter_route = [Helicopter(map, path[0], path[-1])]

    # ⚠️ Verificar disponibilidade dos veículos na capital
    capital_id = path[0]  # A capital é o primeiro nó no caminho
    capital_info = map.get_city_by_id(capital_id)["capital_info"]

    cars_qnt_needed = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
    trucks_qnt_needed = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
    helicopters_qnt_needed = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)

    if (
        capital_info["cars"] < cars_qnt_needed
        and capital_info["trucks"] < trucks_qnt_needed
        and capital_info["helicopters"] < helicopters_qnt_needed
    ):
        print("\nNot enough vehicles available in the capital.")
        return None

    car_cost = sum_vehicles_cost(car_route) if capital_info["cars"] >= cars_qnt_needed else None
    truck_cost = sum_vehicles_cost(truck_route) if capital_info["trucks"] >= trucks_qnt_needed else None
    helicopter_cost = sum_vehicles_cost(helicopter_route) if capital_info["helicopters"] >= helicopters_qnt_needed else None

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
        print("\nNo valid routes available.")
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

def find_path_bfs(map: Map, end_city_id: str):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    nearest_capital = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )
    start_city = nearest_capital

    queue = [start_city]
    visited = set()
    parent = {start_city["id"]: None}

    while queue:
        current_city = queue.pop(0)
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
            if neighbor_id not in visited:
                queue.append(map.get_city_by_id(neighbor_id))
                parent[neighbor_id] = current_city_id

    return None
