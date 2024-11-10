from map import Map
from draw_map import draw_map

from json import load

places = load(open("maps_examples/random_places.json"))
routes = load(open("maps_examples/random_places_routes.json"))

map = Map(places, routes)

draw_map(map)
