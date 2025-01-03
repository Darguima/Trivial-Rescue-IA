from map.map import Map

from vehicles.sum_vehicles_cost import sum_vehicles_cost
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.helicopter import Helicopter
from vehicles.boat import Boat

import math
from typing import List, Callable, Literal


def create_mono_vehicle_routes(
    map: Map,
    capital_city_id: str,
    end_city_id: str,
    groceries_tons: int,
    find_path_function: Callable[
        [Map, str, str, Literal["land", "air", "sea"]], List[str]
    ],
):
    capital_grocery_tons = map.get_city_by_id(capital_city_id)["capital_info"][
        "groceries_tons"
    ]
    groceries_tons = min(groceries_tons, capital_grocery_tons)

    print("\n=====================")
    print(
        f"Finding best route from {capital_city_id} to {end_city_id} with {groceries_tons} tons of groceries."
    )

    land_path = find_path_function(map, capital_city_id, end_city_id, route_type="land")
    air_path = find_path_function(map, capital_city_id, end_city_id, route_type="air")
    sea_path = find_path_function(map, capital_city_id, end_city_id, route_type="sea")

    if land_path is None and air_path is None and sea_path is None:
        print("Path not found.")
        return []

    print("\nLand Path found:", land_path)
    print("Air Path found:", air_path)
    print("Sea Path found:", sea_path)

    routes = []

    cars_qnt_needed = math.ceil(groceries_tons / Car.MAX_CAPACITY_TONS)
    cars_available = map.get_city_by_id(capital_city_id)["capital_info"]["cars"]
    vehicles_used = min(cars_qnt_needed, cars_available)

    if land_path and vehicles_used > 0:
        route = [
            Car(map, land_path[i], land_path[i + 1]) for i in range(len(land_path) - 1)
        ]
        route_cost = sum_vehicles_cost(
            route, [vehicles_used] * len(route), map=map
        ).get_final_cost()
        max_tons_transported = vehicles_used * Car.MAX_CAPACITY_TONS

        routes.append(
            {
                "vehicles_used": vehicles_used,
                "route": route,
                "cost": route_cost,
                "max_tons_transported": max_tons_transported,
            }
        )

    trucks_qnt_needed = math.ceil(groceries_tons / Truck.MAX_CAPACITY_TONS)
    trucks_available = map.get_city_by_id(capital_city_id)["capital_info"]["trucks"]
    vehicles_used = min(trucks_qnt_needed, trucks_available)
    max_tons_transported = vehicles_used * Truck.MAX_CAPACITY_TONS

    if land_path and vehicles_used > 0:
        route = [
            Truck(map, land_path[i], land_path[i + 1])
            for i in range(len(land_path) - 1)
        ]
        route_cost = sum_vehicles_cost(
            route, [vehicles_used] * len(route), map=map
        ).get_final_cost()

        routes.append(
            {
                "vehicles_used": vehicles_used,
                "route": route,
                "cost": route_cost,
                "max_tons_transported": max_tons_transported,
            }
        )

    helicopters_qnt_needed = math.ceil(groceries_tons / Helicopter.MAX_CAPACITY_TONS)
    helicopters_available = map.get_city_by_id(capital_city_id)["capital_info"][
        "helicopters"
    ]
    vehicles_used = min(helicopters_qnt_needed, helicopters_available)
    max_tons_transported = vehicles_used * Helicopter.MAX_CAPACITY_TONS

    if air_path and vehicles_used > 0:
        route = [Helicopter(map, air_path[0], air_path[-1])]
        route_cost = sum_vehicles_cost(route, [vehicles_used], map=map).get_final_cost()

        routes.append(
            {
                "vehicles_used": vehicles_used,
                "route": route,
                "cost": route_cost,
                "max_tons_transported": max_tons_transported,
            }
        )

    boats_qnt_needed = math.ceil(groceries_tons / Boat.MAX_CAPACITY_TONS)
    boats_available = (
        map.get_city_by_id(capital_city_id)["harbor_info"]["boats"]
        if map.get_city_by_id(capital_city_id)["harbor_info"]
        else 0
    )
    vehicles_used = min(boats_qnt_needed, boats_available)
    max_tons_transported = vehicles_used * Boat.MAX_CAPACITY_TONS

    if sea_path and vehicles_used > 0:
        route = [
            Boat(map, sea_path[i], sea_path[i + 1]) for i in range(len(sea_path) - 1)
        ]
        route_cost = sum_vehicles_cost(
            route, [vehicles_used] * len(route), map=map
        ).get_final_cost()

        routes.append(
            {
                "vehicles_used": vehicles_used,
                "route": route,
                "cost": route_cost,
                "max_tons_transported": max_tons_transported,
            }
        )

    routes = sorted(routes, key=lambda route: route["cost"])

    # The best routes will receive the maximum amount of groceries possible
    for route in routes:
        tons_transported = min(groceries_tons, route["max_tons_transported"])
        route["tons_transported"] = tons_transported
        groceries_tons -= tons_transported

    routes = [route for route in routes if route["tons_transported"] > 0]

    print("\nRoutes found (in order of cost relevance):\n")
    for route in routes:
        # create a copy with string vehicles, just to print
        route_copy = route.copy()
        route_copy["route"] = [str(vehicle) for vehicle in route["route"]]
        print(route_copy)
    print()

    return routes
