from random import randint
from json import dump

MATRIX_WIDTH = 8

places = []
routes = []

for i in range(MATRIX_WIDTH ** 2):
  places.append({
    "name": f"Place {i}",
    "district_capital": True,
    "coords": (i % MATRIX_WIDTH, i // MATRIX_WIDTH),
    "population": randint(1000, 1_000_000),
  })

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


for i in range(MATRIX_WIDTH ** 2):
  routes.append([])

  neighbors = []

  if (i - MATRIX_WIDTH >= 0):
    neighbors.append(i - MATRIX_WIDTH)

  if (i % MATRIX_WIDTH != 0):
    neighbors.append(i - 1)

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

with open("maps_examples/random_places.json", "w") as f:
  dump(places, f, indent=2)

with open("maps_examples/random_places_routes.json", "w") as f:
  dump(routes, f, indent=2)