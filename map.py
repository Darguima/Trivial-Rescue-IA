class Map:
  def __init__(self, places, routes):
    self.__places = places
    self.__routes = routes

  def get_place_id_by_name(self, name):
    for place_id, place in enumerate(self.__places):
      if place["name"] == name:
        return place_id
  
  def get_place_by_name(self, name):
      return self.__places[self.get_place_id_by_name(name)]
  
  def get_all_places_ids(self):
    return range(len(self.__places))

  def get_place_by_id(self, id):
    return self.__places[id]

  def get_neighbors_ids_by_place_id(self, id):
    neighbors = {
      "land": [],
      "air": [],
      "sea": []
    } 

    # The neighbors with lower id
    for possible_neighbor_id, possible_neighbor in enumerate(self.__routes[id]):
      if (possible_neighbor["land"] != None):
        neighbors["land"].append(possible_neighbor_id)
      if (possible_neighbor["air"] != None):
        neighbors["air"].append(possible_neighbor_id)
      if (possible_neighbor["sea"] != None):
        neighbors["sea"].append(possible_neighbor_id)
    
    for possible_neighbor_id in range(id + 1, len(self.__routes)):
      possible_neighbor = self.__routes[possible_neighbor_id][id]

      if (possible_neighbor["land"] != None):
        neighbors["land"].append(possible_neighbor_id)
      if (possible_neighbor["air"] != None):
        neighbors["air"].append(possible_neighbor_id)
      if (possible_neighbor["sea"] != None):
        neighbors["sea"].append(possible_neighbor_id)

    return neighbors
  
  def get_route(self, place_a, place_b):
    if place_a == place_b:
      return None
    
    src = max(place_a, place_b)
    dst = min(place_a, place_b)

    if src >= len(self.__routes):
      raise IndexError("The place with the id " + str(src) + " does not exist")

    return self.__routes[src][dst]
