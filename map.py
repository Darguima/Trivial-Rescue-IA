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
    city_id = str(city_id)
    self.__ensure_city_id(city_id)
    return self.__cities.get(str(city_id))

  def get_all_cities(self) -> list[City]:
    """
    Returns a list with all cities on the map.
    """
    return list(self.__cities.values())
  
  def get_routes_between_cities(self, source_id: str, target_id: str) -> RouteBetweenCities:
    """
    Returns the land, air and sea routes between two cities.
    """
    self.__ensure_city_id(source_id)
    self.__ensure_city_id(target_id)

    _source_id = str(source_id)
    _target_id = str(target_id)

    # The routes are stores on a triangle matrix, so we need order the ids
    source_id = str(max(int(_source_id), int(_target_id)))
    target_id = str(min(int(_source_id), int(_target_id)))

    try:
      source_routes = self.__routes[source_id]
      # air routes are stored on a different way
      air_routes = self.__routes[_source_id].get("air", {}).get(_target_id, None)

      r = {
        "land": source_routes.get("land", {}).get(target_id),
        "air": air_routes,
        "sea": source_routes.get("sea", {}).get(target_id)
      }

      return r
    except KeyError as e:
      raise Exception(f"City not found: {e}")
  
  def __ensure_city_id(self, city_id: str):
    city_id = str(city_id)
    if not city_id.isnumeric():
      raise ValueError(f"City ID `{city_id}` must be an integer")