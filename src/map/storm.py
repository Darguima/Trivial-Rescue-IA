import random
from datetime import datetime

# Workaround for circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from map.map import Map
else:

    class Map:
        pass


class Storm:
    def __init__(self, map: Map):
        random.seed(4)

        available_cities = map.get_all_cities()

        self.start_city_id = random.choice(available_cities)["id"]
        self.map = map

        print(f"Storm started at {self.start_city_id}")

    def get_position(self, hours_elapsed: int) -> str:
        steps = int(hours_elapsed / 3)  # Move every 3 hours

        current_city_id = self.start_city_id

        for _ in range(steps):
            current_city = self.map.get_city_by_id(current_city_id)
            neighbors = current_city["neighbors"]["land"]
            if not neighbors:
                break
            current_city_id = random.choice(neighbors)

        return current_city_id
