from _types.map_types import CitiesDict, City, RoutesDict, RouteBetweenCities

class Map:
  def __init__(self, cities, routes):
    self.__cities: CitiesDict = cities
    self.__routes: RoutesDict = routes
  
  def get_city_by_id(self, city_id: str) -> City:
    """
    Will return the city info, given its id.
    If doesn't exist, will return None.
    """
    return self.__cities[str(city_id)]

  def get_all_cities(self) -> list[City]:
    """
    Returns a list with all cities on the map.
    """
    return list(self.__cities.values())
  
  def get_routes_between_cities(self, city_id1: str, city_id2: str) -> RouteBetweenCities:
    """
    Returns the land, air and sea routes between two cities.
    """

    source_id = str(max(int(city_id1), int(city_id2)))
    target_id = str(min(int(city_id1), int(city_id2)))

    source_routes = self.__routes[source_id]

    r = {
      "land": source_routes.get("land", {}).get(target_id),
      "air": source_routes.get("air", {}).get(target_id),
      "sea": source_routes.get("sea", {}).get(target_id)
    }

    return r