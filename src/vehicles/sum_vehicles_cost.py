from typing import List

from vehicles.vehicle import Vehicle
from vehicles.car import Car
from vehicles.truck import Truck


class Cost:
    def __init__(self, time: int, cost: int):
        self.time = time
        self.monetary_cost = cost

    def get_final_cost(self):
        return self.time * 0.8 + self.monetary_cost * 0.2

    def __str__(self):
        return f"Time: {self.time}, Monetary Cost: {self.monetary_cost}. Final Cost: {self.get_final_cost()}"

    def __lt__(self, other):
        return self.get_final_cost() < other.get_final_cost()


def sum_vehicles_cost(vehicles: List[Vehicle]):
    """
    Given a List of instance of Vehicle, return the total cost of the route.
    If for some reason the route is invalid, return None. (e.g. an Helicopter run out of fuel)
    """
    cost = Cost(0, 0)

    if len(vehicles) == 0:
        return cost

    last_vehicle = None
    liters_spent_on_last_vehicle = 0

    for vehicle in vehicles:
        type_vehicle_changed = type(last_vehicle) != type(vehicle)
        vehicle_cost = vehicle.calculate_cost()

        cost.time += vehicle_cost["time"]
        cost.monetary_cost += vehicle_cost["fuel_liters"] * vehicle.FUEL_LITER_COST
        liters_spent_on_last_vehicle += vehicle_cost["fuel_liters"]

        if type_vehicle_changed:
            cost.time += vehicle.TRANSHIPMENT_PENALTY

        if liters_spent_on_last_vehicle > vehicle.TANK_LITERS_CAPACITY:
            if isinstance(vehicle, (Car, Truck)):
                cost.time += vehicle.STOP_PENALTY
                cost.time += vehicle.FILL_TANK_PENALTY
                liters_spent_on_last_vehicle -= vehicle.TANK_LITERS_CAPACITY
            else:
                return None

        last_vehicle = vehicle

    return cost
