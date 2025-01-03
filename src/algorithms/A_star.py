import heapq
import math
from map.map import Map
from utils.distance_between_coords import distance_between_coords
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.sum_vehicles_cost import sum_vehicles_cost


def A_star(map: Map, end_city_id: str, groceries_tons: int):
    capitals = map.get_capitals()
    start_city = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], map.get_city_by_id(end_city_id)["map_coords"]
        ),
    )
    capital_id = start_city["id"]
    capital_info = map.get_city_by_id(capital_id)["capital_info"]

    # Try to find a path using cars
    car_route = find_path(map, end_city_id, vehicle_type="car")
    cars_qnt_needed = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
    if car_route and capital_info["cars"] >= cars_qnt_needed:
        car_route = create_route(map, car_route, Car)
        car_cost = sum_vehicles_cost(
            car_route, [cars_qnt_needed] * len(car_route)
        ).get_final_cost()
    else:
        car_cost = None

    # Try to find a path using trucks
    truck_route = find_path(map, end_city_id, vehicle_type="truck")
    trucks_qnt_needed = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
    if truck_route and capital_info["trucks"] >= trucks_qnt_needed:
        truck_route = create_route(map, truck_route, Truck)
        truck_cost = sum_vehicles_cost(
            truck_route, [trucks_qnt_needed] * len(truck_route)
        ).get_final_cost()
    else:
        truck_cost = None

    # Try to find a path using helicopters
    helicopter_route = find_path(map, end_city_id, vehicle_type="helicopter")
    helicopters_qnt_needed = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)
    if helicopter_route and capital_info["helicopters"] >= helicopters_qnt_needed:
        helicopter_route = create_route(map, helicopter_route, Helicopter)
        helicopter_cost = sum_vehicles_cost(
            helicopter_route, [helicopters_qnt_needed] * len(helicopter_route)
        ).get_final_cost()
    else:
        helicopter_cost = None

    # Print route and cost details
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
        key=lambda option: option[0],
    )

    print(f"\nBest route:")
    print("\tindex:", best_index)
    print("\tfinal cost:", best_cost[0])
    print("\tvehicles needed:", best_cost[1])

    return options[best_index][2]


def find_path(map: Map, end_city_id: str, vehicle_type: str):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    start_city = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )

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
            if vehicle_type == "car" and weather != "land":
                continue
            if vehicle_type == "truck" and weather != "land":
                continue
            if vehicle_type == "helicopter" and weather != "air":
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
