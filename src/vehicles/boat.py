from map.map import Map
from vehicles.vehicle import Vehicle


class Boat(Vehicle):
    MAX_SPEED = 40
    FUEL_LITERS_PER_100KM = 250_000
    FUEL_LITER_COST = 1

    TRANSHIPMENT_PENALTY = 2  # 2 hour
    STOP_PENALTY = 1  # 1 hour
    FILL_TANK_PENALTY = 10
    TANK_LITERS_CAPACITY = 3_000_000

    MAX_CAPACITY_TONS = 10_000

    COLOR = "darkblue"

    def __init__(self, map: Map, starting_node: str, ending_node: str):
        super().__init__(map, starting_node, ending_node)

        self.route = map.get_routes_between_cities(starting_node, ending_node)["sea"]

        if not self.route:
            raise Exception("Route not found")

        self.distance = self.route["distance"]

    def calculate_cost(self):
        max_speed = self.MAX_SPEED

        time = self.distance / max_speed

        fuel_liters = self.distance / 100 * self.FUEL_LITERS_PER_100KM

        return {"time": time, "fuel_liters": fuel_liters}
        
    def __str__(self):
        return f"Boat: {self.starting_node} -> {self.ending_node}"

