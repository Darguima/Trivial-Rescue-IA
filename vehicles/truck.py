# parametros da rota que ainda nao foram usados - catástrofe, transito???, 

class Truck():
  MAX_SPEED = 90
  FUEL_LITERS_PER_100KM = 30
  FUEL_LITER_COST = 1.8

  TRANSHIPMENT_PENALTY  = 0.75 # 45 minutes
  STOP_PENALTY = 0.05 # 3 minutes 
  FILL_TANK_PENALTY = 0.16 # 10 minutes
  TANK_LITERS_CAPACITY = 350

  def __init__(self, map, starting_node, ending_node):
    self.route = map.get_route(starting_node, ending_node)["land"]

    self.distance = self.route["distance"]
    self.road_quality = self.route["road_quality"]
    self.max_speed = self.route["max_speed"]
    self.elevation_diff = self.route["elevation_diff"]

  def calculate_cost(self):
    max_speed = min(self.max_speed, self.MAX_SPEED)


    time = self.distance / max_speed
    time *= 3 - (self.road_quality / 100)
    time *= 2.5 + (self.elevation_diff / 1000) * 2

    fuel_liters = self.distance / 100 * self.FUEL_LITERS_PER_100KM
    fuel_liters  *= 2.5 + (self.elevation_diff / 1000) * 2

    return {
      "time": time,
      "fuel_liters": fuel_liters
    }

