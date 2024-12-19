from abc import ABC, abstractmethod
from map.map import Map

class Vehicle(ABC):
    def __init__(self, map: Map, starting_node: str, ending_node: str):
      ...

    @abstractmethod
    def calculate_cost(self):
      pass

