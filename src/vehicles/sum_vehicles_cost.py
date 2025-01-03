from typing import List

from vehicles.vehicle import Vehicle
from vehicles.car import Car
from vehicles.truck import Truck

from map.map import Map


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


def sum_vehicles_cost(
    vehicles: List[Vehicle],
    list_of_number_of_vehicles: List[int] = None,
    map: Map = None,
) -> Cost:
    """
    Given a List of instance of Vehicle and a corresponding List of the number of vehicles,
    return the total cost of the route.
    If for some reason the route is invalid, return None. (e.g. an Helicopter runs out of fuel)
    """
    if list_of_number_of_vehicles is None:
        list_of_number_of_vehicles = [1] * len(vehicles)

    cost = Cost(0, 0)

    if len(vehicles) == 0 or len(vehicles) != len(list_of_number_of_vehicles):
        return cost

    last_vehicle = None
    liters_spent_on_last_vehicle = 0
    for vehicle, num_vehicles in zip(vehicles, list_of_number_of_vehicles):
        vehicle_cost = vehicle.calculate_cost()
        cost.time += vehicle_cost["time"]

        if map is not None:
            for storm in map.storms:
                storm_city_id = storm.get_position(cost.time)
                if (
                    storm_city_id == vehicle.starting_node
                    or storm_city_id == vehicle.ending_node
                ):
                    print("\033[90mStorm detected. Penalty added\033[0m")
                    cost.time += vehicle_cost["time"] * 0.15

        for _ in range(num_vehicles):  # Iterate for each vehicle of the same type
            type_vehicle_changed = type(last_vehicle) != type(vehicle)
            cost.monetary_cost += vehicle_cost["fuel_liters"] * vehicle.FUEL_LITER_COST
            liters_spent_on_last_vehicle += vehicle_cost["fuel_liters"] / num_vehicles
            if liters_spent_on_last_vehicle > vehicle.TANK_LITERS_CAPACITY:
                if isinstance(vehicle, (Car, Truck)):
                    cost.time += vehicle.STOP_PENALTY
                    cost.time += vehicle.FILL_TANK_PENALTY
                    liters_spent_on_last_vehicle -= vehicle.TANK_LITERS_CAPACITY
                else:
                    return None
            if type_vehicle_changed:
                cost.time += vehicle.TRANSHIPMENT_PENALTY
                liters_spent_on_last_vehicle = 0
            last_vehicle = vehicle

    return cost
