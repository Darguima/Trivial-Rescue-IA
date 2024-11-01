class Map:
  def __init__(self, places, routes):
    self.__places = places
    self.__routes = routes

  def get_place_id_by_name(self, name):
    for place in self.__places:
      if self.__places[place]["name"] == name:
        return place
  
  def get_place_by_name(self, name):
      return self.__places[self.get_place_id_by_name(name)]
  
  def get_all_places_ids(self):
    return list(self.__places.keys())

  def get_place_by_id(self, id):
    return self.__places[id]
  
  def get_route(self, place_a, place_b):
    if place_a == place_b:
      return None
    
    place_a = int(place_a)
    place_b = int(place_b)

    src = max(place_a, place_b)
    dst = min(place_a, place_b)
    return self.__routes[src][dst]
