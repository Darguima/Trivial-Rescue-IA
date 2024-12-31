import math
import heapq

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat

def dijkstra(map: Map, end_city_id: str, groceries_tons: int):
    print("Dijkstra")
    end_city = map.get_city_by_id(end_city_id)

    capitals = map.get_capitals()
    start_city = min(
        capitals,
        key=lambda capital: distance_between_coords(
            capital["map_coords"], end_city["map_coords"]
        ),
    )

    # Initialize costs with infinity
    costs = {city["id"]: (float('inf'), None) for city in map.get_all_cities()}
    costs[start_city["id"]] = (0, start_city["id"])  
    parents = {start_city["id"]: (None, None, 0)}  
    visited = []
    priority_queue = [(0, start_city["id"])]

    while priority_queue:
        current_cost, current_city_id = heapq.heappop(priority_queue)

        if current_city_id in visited:
            continue

        visited.append(current_city_id)
        current_city = map.get_city_by_id(current_city_id)

        if current_city_id == end_city_id:
            break

        for weather, neighbor_ids in current_city["neighbors"].items():
            for neighbor_id in neighbor_ids:
                neighbor = map.get_city_by_id(neighbor_id)
                travel_cost, transport_type, num_vehicles = calculate_travel_cost(
                    map, current_city, neighbor, groceries_tons, weather
                )
                new_cost = current_cost + travel_cost

                if new_cost < costs[neighbor_id][0]:
                    costs[neighbor_id] = (new_cost, current_city_id)
                    parents[neighbor_id] = (current_city_id, transport_type, num_vehicles)
                    heapq.heappush(priority_queue, (new_cost, neighbor_id))

    if end_city_id not in parents:
        return None  

    # Reconstruct the path from start_city to end_city
    path = []
    transports = []
    current_city_id = end_city_id
    while current_city_id is not None:
        parent_city, transport_type, num_vehicles = parents[current_city_id]
        if parent_city is not None:
            transports.append((parent_city, current_city_id, transport_type, num_vehicles))
        path.append(current_city_id)
        current_city_id = parent_city

    path.reverse()
    transports.reverse()

    print("Path found:", path)
    print("Transport used:", transports)
    print("Total cost:", costs[end_city_id][0])

    route = []
    for transport in transports:
        parent_id, neighbor_id, vehicle_type, num_vehicles = transport
        for _ in range(num_vehicles): 
            if vehicle_type == "Car":
                route.append(Car(map, parent_id, neighbor_id))
            elif vehicle_type == "Truck":
                route.append(Truck(map, parent_id, neighbor_id))
            elif vehicle_type == "Helicopter":
                route.append(Helicopter(map, parent_id, neighbor_id))
            elif vehicle_type == "Boat":
                route.append(Boat(map, parent_id, neighbor_id))

    print("Total cost of the route:", sum_vehicles_cost(route))
    print("Route:", route)

    return route

def calculate_travel_cost(map: Map, current_city, neighbor, groceries_tons, weather):
    vehicle_classes = {
        "air": [Helicopter],
        "land": [Car, Truck],
        "water": [Boat]
    }

    # Get the list of vehicles applicable for the given weather
    applicable_vehicles = vehicle_classes.get(weather, [])
    if not applicable_vehicles:
        return float('inf'), None, 0  # Invalid weather type, return infinity cost, no vehicle, and zero vehicles

    # Initialize the minimum cost and corresponding vehicle
    min_cost = float('inf')
    best_vehicle_type = None
    number_of_vehicles_needed = 0

    for vehicle_class in applicable_vehicles:
        vehicle = vehicle_class(map, current_city["id"], neighbor["id"])
        vehicle_cost = vehicle.calculate_cost()

        # Calculate the number of vehicles required

        num_vehicles = math.ceil(groceries_tons / vehicle.MAX_CAPACITY_TONS)

        # Calculate total cost for this option
        total_cost = num_vehicles * (vehicle_cost["time"] * 0.8 +
                                     vehicle_cost["fuel_liters"] * vehicle.FUEL_LITER_COST * 0.2)

        # Update the minimum cost if this option is cheaper
        if total_cost < min_cost:
            min_cost = total_cost
            best_vehicle_type = vehicle_class.__name__  
            number_of_vehicles_needed = num_vehicles

    return min_cost, best_vehicle_type, number_of_vehicles_needed

