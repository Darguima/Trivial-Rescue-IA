from json import load

from map import Map
from interface import interface

print("Loading map data...")

cities_dict = load(open("maps_examples/random_cities.json"))
routes_dict = load(open("maps_examples/random_cities_routes.json"))

map = Map(cities_dict, routes_dict)

while True:
  interface(map)
