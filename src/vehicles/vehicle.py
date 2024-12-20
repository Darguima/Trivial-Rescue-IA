from abc import ABC, abstractmethod
from map.map import Map


class Vehicle(ABC):
    COLOR = "k"

    def __init__(self, map: Map, starting_node: str, ending_node: str):
        self.starting_node = str(starting_node)
        self.ending_node = str(ending_node)

    @abstractmethod
    def calculate_cost(self):
        pass
