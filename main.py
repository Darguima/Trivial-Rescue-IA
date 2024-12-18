from map import Map
from draw_map import draw_map
from json import load
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.boat import Boat
from vehicles.helicopter import Helicopter
from vehicles.sum_vehicles_cost import sum_vehicles_cost

places = load(open("maps_examples/random_places.json"))
routes = load(open("maps_examples/random_places_routes.json"))

map = Map(places, routes)

route = [Car(map, 11, 8), Car(map, 8, 4), Car(map, 4, 5), Car(map, 5, 0), Car(map, 0, 1), Car(map, 1, 2), Truck(map, 2, 7), Truck(map, 7, 9), Helicopter(map, 9, 15)]

print(map.get_route(0, 1)["land"])
print(map.get_route(1, 2)["land"])
print(map.get_route(2, 7)["land"])
print(map.get_route(7, 9)["land"])
print(map.get_route(9, 15)["air"])

print(sum_vehicles_cost(route))

draw_map(map)
