from map.map import Map


def dionisio(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path(map, end_city_id)

    print("\nPath found:", path)

    # must return a list of vehicles - to draw the path, or None if it wasnt possible to find a path
    # example of return - [Car(map, 0, 1), Car(...), Truck(...), Helicopter(...)]
    return path


def find_path(map: Map, end_city_id: str):
    return []
