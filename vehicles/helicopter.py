from map import Map

class Helicopter():
  MAX_SPEED = 300
  FUEL_LITERS_PER_100KM = 350
  FUEL_LITER_COST = 2

  TRANSHIPMENT_PENALTY  = 0.75 # 45 minutes
  STOP_PENALTY = 1 # 1 hour 
  FILL_TANK_PENALTY = 0.12 # 7 minutes
  TANK_LITERS_CAPACITY = 2_500

  def __init__(self, map: Map, starting_node: str, ending_node: str):
    self.route = map.get_routes_between_cities(starting_node, ending_node)["air"]

    if not self.route:
      raise Exception("Route not found")

    self.distance = self.route["distance"]

  def calculate_cost(self):
    max_speed = self.MAX_SPEED

    time = self.distance / max_speed

    fuel_liters = self.distance / 100 * self.FUEL_LITERS_PER_100KM

    return {
      "time": time,
      "fuel_liters": fuel_liters
    }
