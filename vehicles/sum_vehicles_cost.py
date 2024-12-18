from vehicles.car import Car
from typing import List

def sum_vehicles_cost(vehicles: List[Car]):
  cost = {
    "time": 0,
    "cost": 0,
  }

  if len(vehicles) == 0:
    return cost

  last_vehicle = None
  liters_spent_on_last_vehicle = 0

  for vehicle in vehicles:
    type_vehicle_changed = type(last_vehicle) != type(vehicle)
    vehicle_cost = vehicle.calculate_cost()

    cost["time"] += vehicle_cost["time"]
    cost["cost"] += vehicle_cost["fuel_liters"] * vehicle.FUEL_LITER_COST
    liters_spent_on_last_vehicle += vehicle_cost["fuel_liters"]

    if type_vehicle_changed:
      cost["time"] += vehicle.TRANSHIPMENT_PENALTY
  
    print(liters_spent_on_last_vehicle, vehicle.TANK_LITERS_CAPACITY)
    if liters_spent_on_last_vehicle > vehicle.TANK_LITERS_CAPACITY:
      print("FILLING TANK")
      cost["time"] += vehicle.STOP_PENALTY
      cost["time"] += vehicle.FILL_TANK_PENALTY
      liters_spent_on_last_vehicle -= vehicle.TANK_LITERS_CAPACITY

    last_vehicle = vehicle
  
  return cost
