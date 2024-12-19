from map import Map
from vehicles.vehicle import Vehicle

class Boat(Vehicle):
  MAX_SPEED = 40
  FUEL_LITERS_PER_100KM = 250_000
  FUEL_LITER_COST = 1
  
  TRANSHIPMENT_PENALTY = 2 # 2 hour
  STOP_PENALTY = 1 # 1 hour 
  FILL_TANK_PENALTY = 10
  TANK_LITERS_CAPACITY = 3_000_000

  def __init__(self, map: Map, starting_node: str, ending_node: str):
    self.route = map.get_route(starting_node, ending_node)["sea"]

    if not self.route:
      raise Exception("Route not found")

    print(self.route)

  def calculate_cost(self):
    # max_speed = min(self.max_speed, TRUCK_MAX_SPEED)

    # time = self.distance / max_speed
    # time *= 3 - (self.road_quality / 100)
    # time *= 2.5 + (self.elevation_diff / 1000) * 2

    # fuel_liters = self.distance / 100 * TRUCK_FUEL_FUEL_LITERS_PER_100KM
    # fuel_liters  *= 2.5 + (self.elevation_diff / 1000) * 2

    # return {
    #   "time": time,
    #   "fuel_liters": fuel_liters,
    # }

    return {
      "time": 0,
      "fuel_liters": 0
    }
