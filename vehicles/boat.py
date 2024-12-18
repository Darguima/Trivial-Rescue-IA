# parametros da rota que ainda nao foram usados - catástrofe

class Boat():
  MAX_SPEED = 40
  FUEL_LITERS_PER_100KM = 250_000
  FUEL_LITER_COST = 1
  
  TRANSHIPMENT_PENALTY = 2 # 2 hour
  STOP_PENALTY = 1 # 1 hour 
  FILL_TANK_PENALTY = 10
  TANK_LITERS_CAPACITY = 3_000_000

  def __init__(self, map, starting_node, ending_node):
    self.route = map.get_route(starting_node, ending_node)["sea"]

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
