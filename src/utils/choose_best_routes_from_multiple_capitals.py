from map.map import Map

from typing import List, Callable, Literal

from utils.create_mono_vehicle_routes import create_mono_vehicle_routes


def choose_best_routes_from_multiple_capitals(
    map: Map,
    nearest_capitals: List[dict],
    end_city_id: str,
    groceries_tons: int,
    find_path_function: Callable[
        [Map, str, str, Literal["land", "air", "sea"]], List[str]
    ],
) -> List[dict]:
    tons_transported = 0
    i = 0
    possible_routes = []

    while (tons_transported < groceries_tons or i < 2) and len(nearest_capitals) > 0:
        current_capital = nearest_capitals.pop(0)
        capital_id = current_capital["id"]

        routes = create_mono_vehicle_routes(
            map, capital_id, end_city_id, groceries_tons, find_path_function
        )
        possible_routes += routes

        print(routes)

        for route in routes:
            tons_transported += route["tons_transported"]

        print(f"\n{tons_transported} tons transported so far.")

    if tons_transported < groceries_tons:
        print("\nNot enough groceries transported.")

    possible_routes = sorted(possible_routes, key=lambda route: route["cost"])

    # Choose the best routes, until all the groceries are transported
    multiple_routes = []
    tons_transported = 0
    total_cost = 0
    for route in possible_routes:
        tons_transported += route["tons_transported"]
        total_cost += route["cost"]
        multiple_routes.append(route)
        if tons_transported >= groceries_tons:
            break

    print("\n=====================")
    print(f"\nRoutes used: (Total Cost: {total_cost})\n")
    for route in multiple_routes:
        # create a copy with string vehicles, just to print
        route_copy = route.copy()
        route_copy["route"] = [str(vehicle) for vehicle in route["route"]]
        print(route_copy)
    print()

    return multiple_routes
