from random import randint
from json import dump

MATRIX_WIDTH = 20
MAP_VOID_PROBABILITY = 20

places = []
coords_to_id = {}
routes = []

print("Generating random places.")
id = 0
for coords_seed in range(MATRIX_WIDTH ** 2):
  place_exists = randint(1, 100) > MAP_VOID_PROBABILITY

  if (not place_exists):
    continue

  coords = (coords_seed % MATRIX_WIDTH, coords_seed // MATRIX_WIDTH)
  places.append({
    "name": f"Place {id}",
    "district_capital": True,
    "coords": coords,
    "population": randint(1000, 1_000_000),
  })

  coords_key = f"({coords[0]}, {coords[1]})"
  coords_to_id[coords_key] = id
  id += 1

print("Random places generated.")
# viana_to_braga = {
#   # is needed to think about the elevation_diff, because it depends on the direction
#   # road_quality is a percentage
#   # current_catastrophes should be of another type, like an enum
#   "land": {"distance": 60, "road_quality": 80, "max_speed": 120, "elevation_diff": 100},
#   "air": {"distance": 50},
#   "sea": {"distance": 50},
# }

# Terrestre - qualidade rota, elevação, catástrofe, velocidade maxima, distancia, transito???, 
# Aéreo - distancia, catastrofe
# Maritimo - distancia, catastrofe

print("Calculating routes.")
for i, place in enumerate(places):
  print(f"Generated {i}/{len(places)}.", end="\r")
  routes.append([])

  place_x, place_y = place["coords"]

  neighbors = []

  top_neighbor = coords_to_id.get(f"({place_x}, {place_y - 1})")
  if (top_neighbor != None):
    neighbors.append(top_neighbor)

  left_neighbor = coords_to_id.get(f"({place_x - 1}, {place_y})")
  if (left_neighbor != None):
    neighbors.append(left_neighbor)

  for j in range(i):
    land = None

    if (j in neighbors):
      average_population = (places[i]["population"] + places[j]["population"]) / 2

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

      land = {
        "distance": randint(50, 100),
        "road_quality": road_quality,
        "max_speed": max_speed,
        "elevation_diff": randint(-100, 100),
      }

    routes[i].append({
      "land": land,
      "air": None,
      "sea": None,
    })

print("Routes calculated.")

print("Saving places to files.")
with open("src/maps_examples/random_places.json", "w") as f:
  dump(places, f)

print("Saving routes to files.")
with open("src/maps_examples/random_places_routes.json", "w") as f:
  dump(routes, f)