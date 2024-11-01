from map import Map

places = {
  "0": {
    "name": "Viana do Castelo",
    "district_capital": True,
    "coords": (41.6932, -8.8326),
    "population": 88_725,
  },

  "1": {
    "name": "Braga",
    "district_capital": True,
    "coords": (41.5333, -8.4167),
    "population": 181_819,
  },

  "2": {
    "name": "Famalicão",
    "district_capital": False,
    "coords": (41.3000, -7.7333),
    "population": 50_110,
  },

  "3": {
    "name": "Guimarães",
    "district_capital": False,
    "coords": (41.4416, -8.2950),
    "population": 158_124,
  }
}

viana_to_braga = {
  # is needed to think about the elevation_diff, because it depends on the direction
  # road_quality is a percentage
  # current_catastrophes should be of another type, like an enum
  "land": {"distance": 60, "road_quality": 80, "max_speed": 120, "elevation_diff": 100},
  "air": {"distance": 50},
  "sea": {"distance": 50},
}

viana_to_famalicao = {
  "land": {"distance": 70, "road_quality": 75, "max_speed": 110, "elevation_diff": 120},
  "air": {"distance": 60},
  "sea": {"distance": 60},
}

braga_to_famalicao = {
  "land": {"distance": 20, "road_quality": 85, "max_speed": 100, "elevation_diff": 50},
  "air": {"distance": 15},
  "sea": {"distance": 15},
}

viana_to_guimaraes = {
  "land": {"distance": 80, "road_quality": 70, "max_speed": 100, "elevation_diff": 150},
  "air": {"distance": 70},
  "sea": {"distance": 70},
}

braga_to_guimaraes = {
  "land": {"distance": 25, "road_quality": 90, "max_speed": 120, "elevation_diff": 60},
  "air": {"distance": 20},
  "sea": {"distance": 20},
}

famalicao_to_guimaraes = {
  "land": {"distance": 30, "road_quality": 80, "max_speed": 110, "elevation_diff": 70},
  "air": {"distance": 25},
  "sea": {"distance": 25},
}

routes = [
  [],
  [viana_to_braga],
  [viana_to_famalicao, braga_to_famalicao],
  [viana_to_guimaraes, braga_to_guimaraes, famalicao_to_guimaraes]
]

map = Map(places, routes)

viana_id = map.get_place_id_by_name("Viana do Castelo")
viana = map.get_place_by_id(viana_id)
braga_id = map.get_place_id_by_name("Braga")
famalicao_id = map.get_place_id_by_name("Famalicão")
guimaraes_id = map.get_place_id_by_name("Guimarães")

print(viana_id)
print(viana)

all_places_ids = map.get_all_places_ids()
print(all_places_ids)

viana_to_braga = map.get_route(viana_id, braga_id)
print(viana_to_braga)
