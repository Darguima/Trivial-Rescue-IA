import math

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat


def greedy(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path(map, end_city_id)
    route1 = []  # Cars + fallback to helicopter/boat
    route2 = []  # Trucks + fallback to helicopter/boat
    num_vehicles_route1 = []
    num_vehicles_route2 = []

    if path is None:
        print("\nNo path found.")
        return None

    print("\nPath found:", path)

    # Iterate over the pairs of consecutive cities in the path
    for i in range(len(path) - 1):
        current_city_id = path[i]
        next_city_id = path[i + 1]

        current_city = map.get_city_by_id(current_city_id)
        distance = distance_between_coords(
            current_city["map_coords"], map.get_city_by_id(next_city_id)["map_coords"]
        )

        # Route 1: Prefer Cars, fallback to Helicopter or Boat
        for weather, neighbor_cities in current_city["neighbors"].items():
            if next_city_id in neighbor_cities:
                if weather == "land":
                    

                    num_vehicles = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
                    num_vehicles_route1.append(num_vehicles)

                    car = Car(map, current_city_id, next_city_id)

                    route1.append(car)
                    break

                elif weather == "air":
                    num_vehicles = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)
                    num_vehicles_route1.append(num_vehicles)
                    route1.append(Helicopter(map, current_city_id, next_city_id))
                    break

                elif weather == "water":
                    num_vehicles = math.ceil(groceries_tons / Boat.MAX_CAPACITY_TONS)
                    num_vehicles_route1.append(num_vehicles)
                    route1.append(Boat(map, current_city_id, next_city_id))
                    break

        # Route 2: Prefer Trucks, fallback to Helicopter or Boat
        for weather, neighbor_cities in current_city["neighbors"].items():
            if next_city_id in neighbor_cities:
                if weather == "land":
                    num_vehicles = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
                    num_vehicles_route2.append(num_vehicles)

                    truck = Truck(map, current_city_id, next_city_id)

                    route2.append(truck)
                    break

                elif weather == "air":
                    num_vehicles = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)
                    num_vehicles_route2.append(num_vehicles)
                    route2.append(Helicopter(map, current_city_id, next_city_id))
                    break

                elif weather == "water":
                    num_vehicles = math.ceil(groceries_tons / Boat.MAX_CAPACITY_TONS)
                    num_vehicles_route2.append(num_vehicles)
                    route2.append(Boat(map, current_city_id, next_city_id))
                    break

    # Calculate costs for both routes
    route1_cost = sum_vehicles_cost(route1, num_vehicles_route1)
    route2_cost = sum_vehicles_cost(route2, num_vehicles_route2)

    route1_cost = route1_cost.get_final_cost() 
    route2_cost = route2_cost.get_final_cost()
   
    # Print route and cost details
    print("\nRoute1 (Cars preferred):", route1)
    print("Route2 (Trucks preferred):", route2)
    print("\nRoute1 cost:", route1_cost)
    print("Route2 cost:", route2_cost)

    # Return the cheaper route
    return route1 if route1_cost < route2_cost else route2

def find_path(map: Map, end_city_id: str):
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    start_city = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )

    open_list = set([start_city["id"]])
    visited = set([start_city["id"]])
    parent = {start_city["id"]: None}
    current_city = start_city

    while open_list:
        current_city = min_heuristic(map, current_city, end_city, visited, avoid_air_routes=True)
        if current_city is None:
            return None
        print("current_city",current_city)
        if current_city["id"] == end_city_id:
            # Construct the route
            route = []
            while current_city is not None:
                route.append(current_city["id"])
                current_city = map.get_city_by_id(parent[current_city["id"]]) if parent.get(current_city["id"]) else None
            route.append(start_city["id"])
            route.reverse()

            return route

        for weather, neighbor_ids in current_city["neighbors"].items():
            for neighbor_id in neighbor_ids:
                if neighbor_id not in open_list and neighbor_id not in visited:
                    open_list.add(neighbor_id)
                    parent[neighbor_id] = current_city["id"]

        visited.add(current_city["id"])
        open_list.discard(current_city["id"])

    return None  # Return None if no path is found


def min_heuristic(map: Map, city, end_city, visited, avoid_air_routes=False):
    heuristic_list = []

    for weather, neighbor_ids in city["neighbors"].items():
        for neighbor_id in neighbor_ids:
            aux_city = map.get_city_by_id(neighbor_id)
            if neighbor_id not in visited:
                # Avoid air routes unless explicitly allowed
                if avoid_air_routes and weather == "air":
                    continue
                heuristic = distance_between_coords(
                    aux_city["map_coords"], end_city["map_coords"]
                )
                heuristic_list.append((heuristic, aux_city, weather))

    if not heuristic_list:
        # If no valid neighbors and air routes were ignored, consider air routes now
        if avoid_air_routes:
            return min_heuristic(map, city, end_city, visited, avoid_air_routes=False)
        return None  # No valid neighbors

    heuristic_list.sort(key=lambda x: (x[0], x[2] == "air"))  # Sort by heuristic, prioritizing non-air routes

    return heuristic_list[0][1]  # Return the city with the minimum heuristic
