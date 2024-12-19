from random import randint
from json import dump
from collections import defaultdict
import heapq
import math
from utils.distance_between_coords import distance_between_coords

MATRIX_WIDTH = 5 # Will exists MATRIX_WIDTH ** 2 spaces to cities in the map
SPACE_SIZE = 50 # Each space will be a 50x50 km² square (each space can contain one city)
MAP_VOID_PROBABILITY = 10 # what % of spaces will be empty
NOT_ROAD_PROBABILITY = 15 # what % of roads will not be created
CAPITALS_PERCENTAGE = 2 # what % of the cities will be capitals
CAPITALS_QNT = math.ceil(MATRIX_WIDTH ** 2 * CAPITALS_PERCENTAGE / 100)

def calculate_road_specs(average_population: float) -> int:
  if (average_population > 700_000):
    max_speed = 120
    road_quality = randint(50, 100)
  elif (average_population > 450_000):
    max_speed = 100
    road_quality = randint(50, 90)
  elif (average_population > 200_000):
    max_speed = 90
    road_quality = randint(45, 80)
  else:
    max_speed = 50
    road_quality = randint(30, 70)

  return max_speed, road_quality

places = defaultdict(dict)
routes = defaultdict(dict)

# Aux Structs
coords_to_id = defaultdict(dict) # {0: {2: 5}} - the coords (0, 2) have the node number 5
biggest_cities = [] # min heap with most populated cities

print(f"Generating random cities.", end="\r")

id = 0
for space_i in range(MATRIX_WIDTH ** 2):
  print(f"Generating random cities. {space_i / (MATRIX_WIDTH ** 2) * 100:.2f}%", end="\r")

  # Generate the city
  place_exists = randint(1, 100) > MAP_VOID_PROBABILITY

  if (not place_exists):
    continue

  matrix_coords = (space_i % MATRIX_WIDTH, space_i // MATRIX_WIDTH)
  map_coords = (
    matrix_coords[0] * SPACE_SIZE + randint(0, SPACE_SIZE),
    matrix_coords[1] * SPACE_SIZE + randint(0, SPACE_SIZE),
  )

  population = randint(1000, 1_000_000)
  elevation = randint(-100, 100)

  places[id] = {
    "id": str(id),
    "name": f"Place {id}",
    "capital_info": None,
    "matrix_coords": matrix_coords,
    "map_coords": map_coords,
    "population": population,
    "elevation": elevation,
    "neighbors": {
      "land": [],
      "air": [],
      "sea": [],
    },
  }

  # Aux Structs update
  coords_to_id[matrix_coords[1]][matrix_coords[0]] = id
  if len(coords_to_id) > 2:
    del coords_to_id[min(list(coords_to_id.keys()))]
  
  heapq.heappush(biggest_cities, (population, id))
  if len(biggest_cities) > CAPITALS_QNT:
    heapq.heappop(biggest_cities)
  
  # Routes
  neighbors = []

  vertical_neighbor = coords_to_id.get(matrix_coords[1] - 1, {}).get(matrix_coords[0])
  if vertical_neighbor != None and randint(1, 100) > NOT_ROAD_PROBABILITY:
    neighbors.append(vertical_neighbor)

  horizontal_neighbor = coords_to_id.get(matrix_coords[1], {}).get(matrix_coords[0] - 1)
  if horizontal_neighbor != None and randint(1, 100) > NOT_ROAD_PROBABILITY:
    neighbors.append(horizontal_neighbor)

  places[id]["neighbors"]["land"].extend(neighbors)
  routes[id]["land"] = {}

  for neighbor in neighbors:
    places[neighbor]["neighbors"]["land"].append(id)

    average_population = (population + places[neighbor]["population"]) / 2
    line_distance = distance_between_coords(map_coords, places[neighbor]["map_coords"])
    elevation_diff = elevation - places[neighbor]["elevation"]

    max_speed, road_quality = calculate_road_specs(average_population)

    routes[id]["land"][neighbor] = {
      "distance": line_distance * randint(105, 110) / 100,
      "road_quality": road_quality,
      "max_speed": max_speed,
      "elevation_diff": elevation_diff,
    }

  id += 1

print("")

# Capital cities
print("Converting cities to capital.")
for _, city_id in biggest_cities:
  places[city_id]["capital_info"] = {
    "groceries_tons": randint(1, 25),
    "cars": randint(1, 10),
    "trucks": randint(1, 5),
    "helicopters": randint(1, 3),
  }

print("Random places generated.")

print("Saving places to files.")
with open("maps_examples/random_places.json", "w") as f:
  dump(places, f)

print("Saving routes to files.")
with open("maps_examples/random_places_routes.json", "w") as f:
  dump(routes, f)
