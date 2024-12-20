from json import load

from map.map import Map
from interface.interface import interface

print("Loading map data...")

cities_dict = load(open("src/maps_examples/random_cities.json"))
routes_dict = load(open("src/maps_examples/random_cities_routes.json"))

map = Map(cities_dict, routes_dict)

while True:
    interface(map)
