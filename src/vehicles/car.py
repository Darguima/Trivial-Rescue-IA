from map.map import Map
from vehicles.vehicle import Vehicle


class Car(Vehicle):
    MAX_SPEED = 200
    FUEL_LITERS_PER_100KM = 6
    FUEL_LITER_COST = 1.8

    TRANSHIPMENT_PENALTY = 0.15  # 9 minutes
    STOP_PENALTY = 0.025  # 1:30 minutes
    FILL_TANK_PENALTY = 0.033  # 2 minutes
    TANK_LITERS_CAPACITY = 50

    MAX_CAPACITY_TONS = 0.5

    COLOR = "cyan"

    def __init__(self, map: Map, starting_node: str, ending_node: str):
        super().__init__(map, starting_node, ending_node)

        self.route = map.get_routes_between_cities(starting_node, ending_node)["land"]

        if not self.route:
            raise Exception("Route not found")

        self.distance = self.route["distance"]
        self.road_quality = self.route["road_quality"]
        self.max_speed = self.route["max_speed"]
        self.elevation_diff = self.route["elevation_diff"]

    def calculate_cost(self):
        max_speed = min(self.max_speed, self.MAX_SPEED)

        time = self.distance / max_speed
        time *= 2 - (self.road_quality / 100)
        time *= 1.5 + (self.elevation_diff / 1000) * 2

        fuel_liters = self.distance / 100 * self.FUEL_LITERS_PER_100KM
        fuel_liters *= 1.5 + (self.elevation_diff / 1000) * 2

        return {"time": time, "fuel_liters": fuel_liters}

    def __str__(self):
        return f"Car: {self.starting_node} -> {self.ending_node}"