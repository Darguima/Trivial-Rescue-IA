from random import randint
from json import dump
from collections import defaultdict
import heapq
import math
from utils.distance_between_coords import distance_between_coords
from _types.map_types import CitiesDict, RoutesDict

MATRIX_WIDTH = 7  # Will exists MATRIX_WIDTH ** 2 spaces to cities in the map
SPACE_SIZE = (
    50  # Each space will be a 50x50 km² square (each space can contain one city)
)
MAP_VOID_PROBABILITY = 10  # what % of spaces will be empty
NOT_ROAD_PROBABILITY = 15  # what % of roads will not be created
NOT_HARBOR_PROBABILITY = 15  # what % of cities will not have a harbor
CAPITALS_PERCENTAGE = 2  # what % of the cities will be capitals
CAPITALS_QNT = math.ceil(MATRIX_WIDTH**2 * CAPITALS_PERCENTAGE / 100)

def calculate_road_specs(average_population: float) -> int:
    if average_population > 700_000:
        max_speed = 120
        road_quality = randint(50, 100)
    elif average_population > 450_000:
        max_speed = 100
        road_quality = randint(50, 90)
    elif average_population > 200_000:
        max_speed = 90
        road_quality = randint(45, 80)
    else:
        max_speed = 50
        road_quality = randint(30, 70)

    return max_speed, road_quality


cities: CitiesDict = defaultdict(dict)
routes: RoutesDict = defaultdict(dict)

# Aux Structs
coords_to_id = defaultdict(
    dict
)  # {0: {2: 5}} - the coords (0, 2) have the node number 5
capital_cities = [] # min heap with most populated cities
coastal_cities = [] # list of cities that are coastal

print(f"Generating random cities.", end="\r")

id = "0"
for space_i in range(MATRIX_WIDTH**2):
    print(
        f"Generating random cities. {space_i / (MATRIX_WIDTH ** 2) * 100:.2f}%",
        end="\r",
    )

    # Generate the city
    matrix_coords = (space_i % MATRIX_WIDTH, space_i // MATRIX_WIDTH)
    map_coords = (
        matrix_coords[0] * SPACE_SIZE + randint(0, SPACE_SIZE),
        matrix_coords[1] * SPACE_SIZE + randint(0, SPACE_SIZE),
    )

    city_exists = randint(1, 100) > MAP_VOID_PROBABILITY

    if not city_exists:
        # add sea neighbors to coastal cities
        if matrix_coords[0] - 1 >= 0:
            left_neighbor = coords_to_id.get(matrix_coords[1], {}).get(
                matrix_coords[0] - 1
            )
            if left_neighbor != None:
                coastal_cities.append(left_neighbor)
        if matrix_coords[1] - 1 >= 0:
            bottom_neighbor = coords_to_id.get(matrix_coords[1] - 1, {}).get(
                matrix_coords[0]
            )
            if bottom_neighbor != None:
                coastal_cities.append(bottom_neighbor)
        continue

    population = randint(1000, 1_000_000)
    elevation = randint(-100, 100)

    cities[id] = {
        "id": id,
        "name": f"City {id}",
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

    heapq.heappush(capital_cities, (population, id))
    if len(capital_cities) > CAPITALS_QNT:
        heapq.heappop(capital_cities)

    # Routes
    neighbors = []

    bottom_neighbor = coords_to_id.get(matrix_coords[1] - 1, {}).get(matrix_coords[0])
    if bottom_neighbor != None and randint(1, 100) > NOT_ROAD_PROBABILITY:
        neighbors.append(bottom_neighbor)
    elif bottom_neighbor == None and matrix_coords[1] - 1 >= 0:
        coastal_cities.append(id)

    left_neighbor = coords_to_id.get(matrix_coords[1], {}).get(
        matrix_coords[0] - 1
    )
    if left_neighbor != None and randint(1, 100) > NOT_ROAD_PROBABILITY:
        neighbors.append(left_neighbor)
    elif left_neighbor == None and matrix_coords[0] - 1 >= 0:
        coastal_cities.append(id)

    cities[id]["neighbors"]["land"].extend(neighbors)
    routes[id]["land"] = {}

    for neighbor in neighbors:
        cities[neighbor]["neighbors"]["land"].append(id)

        average_population = (population + cities[neighbor]["population"]) / 2
        line_distance = distance_between_coords(
            map_coords, cities[neighbor]["map_coords"]
        )
        elevation_diff = elevation - cities[neighbor]["elevation"]

        max_speed, road_quality = calculate_road_specs(average_population)

        routes[id]["land"][neighbor] = {
            "distance": line_distance * randint(145, 155) / 100,
            "road_quality": road_quality,
            "max_speed": max_speed,
            "elevation_diff": elevation_diff,
        }

    id = str(int(id) + 1)

print("Generated random cities. 100%    ")

# Capital cities
print("Converting cities to capitals.", end="\r")

capitals_ids = [city_id for _, city_id in capital_cities]
non_capitals_ids = [city_id for city_id in cities if city_id not in capitals_ids]

for i, capital_id in enumerate(capitals_ids):
    print(
        f"Converting cities to capitals. {i / len(capitals_ids) * 100:.2f}%", end="\r"
    )
    cities[capital_id]["capital_info"] = {
        "groceries_tons": randint(1, 25),
        "cars": randint(1, 10),
        "trucks": randint(1, 5),
        "helicopters": randint(1, 3),
    }

    cities[capital_id]["neighbors"]["air"] = non_capitals_ids

    routes[capital_id]["air"] = {}

    for neighbor in non_capitals_ids:
        line_distance = distance_between_coords(
            cities[capital_id]["map_coords"], cities[neighbor]["map_coords"]
        )

        routes[capital_id]["air"][neighbor] = {
            "distance": line_distance * randint(105, 110) / 100,
        }

print("Converted cities to capitals. 100%    ")

# Coastal cities
print("Founding sea routes.", end="\r")

coastal_cities = list(map(str, sorted(set(map(int, coastal_cities)), reverse=True)))
harbor_cities = [harbor for harbor in coastal_cities if randint(0, 100) > NOT_HARBOR_PROBABILITY]

for i in range(len(harbor_cities)):
    source_id = coastal_cities[i]
    routes[source_id]["sea"] = {}
    for j in range(i + 1, len(harbor_cities)):
        destination_id = coastal_cities[j]
        distance = distance_between_coords(cities[source_id]["map_coords"], cities[destination_id]["map_coords"])

        routes[source_id]["sea"][destination_id] = {"distance": distance}
        cities[source_id]["neighbors"]["sea"].append(destination_id)
        cities[destination_id]["neighbors"]["sea"].append(source_id)

print("Sea Routes Found. 100%    ")

print("Saving cities to files.")
with open("src/maps_examples/random_cities.json", "w") as f:
    dump(cities, f)

print("Saving routes to files.")
with open("src/maps_examples/random_cities_routes.json", "w") as f:
    dump(routes, f)
