from map import Map
from draw_map import draw_map
from json import load
from vehicles.car import Car
from vehicles.truck import Truck
from vehicles.sum_vehicles_cost import sum_vehicles_cost

cities_dict = load(open("maps_examples/random_places.json"))
routes_dict = load(open("maps_examples/random_places_routes.json"))

map = Map(cities_dict, routes_dict)

print(map.get_city_by_id(0))
# print(map.get_all_cities())
print(map.get_routes_between_cities(0, 1))

route = [Car(map, 11, 7), Car(map, 7, 2), Truck(map, 2, 1), Truck(map, 1, 0)]

print(sum_vehicles_cost(route))

draw_map(map)
