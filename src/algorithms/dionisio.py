from map.map import Map


def dionisio(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path(map, end_city_id)

    print("\nPath found:", path)

    # must return a list of the cities ids that are part of the path, in order, to draw the path
    # or none if the path is not possible
    return path


def find_path(map: Map, end_city_id: str):
    return []
