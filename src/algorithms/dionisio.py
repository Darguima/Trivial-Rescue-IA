import math

from map.map import Map
from utils.distance_between_coords import distance_between_coords

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat

def dionisio(map: Map, end_city_id: str, groceries_tons: int):
    path = greedy(map, end_city_id)
    route1 = []
    route2 = []
    number_of_vehicles = list()

    if path is None:
        print("\nNo path found.")
        return None

    print("\nPath found:", path)

    # Iterar sobre os pares consecutivos de cidades no caminho
    for i in range(len(path) - 1):
        current_city_id = path[i]
        next_city_id = path[i + 1]

        current_city = map.get_city_by_id(current_city_id)
        
        # Iterar pelos vizinhos da cidade atual
        for weather, neighbor_cities in current_city["neighbors"].items():
            if next_city_id in neighbor_cities:
                # Determinar o meio de transporte com base no clima
                if weather == "air":
                    number_of_vehicles.append(math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS))
                    route1.append(Helicopter(map, current_city_id, next_city_id))
                    route2.append(Helicopter(map, current_city_id, next_city_id))
                elif weather == "land":
                    number_of_vehicles.append(math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS))
                    route1.append(Truck(map, current_city_id, next_city_id))
                    route2.append(Car(map, current_city_id, next_city_id))
                elif weather == "water":
                    number_of_vehicles.append(math.ceil(groceries_tons / Boat.MAX_CAPACITY_TONS))
                    route1.append(Boat(map, current_city_id, next_city_id))
                    route2.append(Boat(map, current_city_id, next_city_id))

    # Exibir as rotas finais
    print("\nRoute1:", route1)
    print("Route2:", route2)



    rota1= sum_vehicles_cost(route1, number_of_vehicles)
    rota2= sum_vehicles_cost(route2, number_of_vehicles)

    print("\nRoute1 cost:", rota1.get_final_cost())
    print("Route2 cost:", rota2.get_final_cost())

    if rota1.get_final_cost() < rota2.get_final_cost():
        return route1
    else:
        return route2



def greedy(map: Map, end_city_id: str):
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
        current_city = min_heuristic(map, current_city, visited)
        if current_city is None:
            return None  

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


def min_heuristic(map: Map, city, visited):
    heuristic_list = []

    for _, neighbor_ids in city["neighbors"].items():
        for neighbor_id in neighbor_ids:
            if neighbor_id not in visited:
                aux_city = map.get_city_by_id(neighbor_id)
                heuristic = distance_between_coords(
                    aux_city["map_coords"], city["map_coords"]
                )
                heuristic_list.append((heuristic, aux_city))

    if not heuristic_list:
        return None  # No valid neighbors

    heuristic_list.sort(key=lambda x: x[0])

    return heuristic_list[0][1]  # Return the city with the minimum heuristic
