from map.map import Map


def breath_first_search(map: Map, end_city_id: str, groceries_tons: int):
    path = find_path(map, end_city_id)

    print("\nPath found:", path)


def find_path(map: Map, end_city_id: str):
    return []
