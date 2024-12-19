from typing import List
from vehicles.vehicle import Vehicle
from vehicles.sum_vehicles_cost import sum_vehicles_cost

def choose_best_route(routes: List[List[Vehicle]]) -> List[Vehicle]:
  def combined_cost(route: List[Vehicle]) -> float:
    cost = sum_vehicles_cost(route)
    return cost["time"] * 0.8 + cost["cost"] * 0.2
  
  best_index, best_route = min(enumerate(routes), key=lambda x: combined_cost(x[1]))

  return best_index, best_route