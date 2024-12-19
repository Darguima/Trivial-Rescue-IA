from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps

from map import Map
from draw_map import draw_map
from vehicles.car import Car
from vehicles.sum_vehicles_cost import sum_vehicles_cost

from algorithms.DFS import depth_first_search

def interface(map: Map):
  clear()
  print("=====================================")
  print("            Trivial Rescue           ")
  print("=====================================\n")

  print("Select an option:\n")

  print("1. Draw matrix map")
  print("2. Draw real map")
  print("3. Get Info about city")
  print("4. Get Info about route")
  print("5. Depth First Search")
  print("6. Code Examples")

  option = input("\nOption: ")

  if option == "1":
    job_for_another_core = multiprocessing.Process(target=draw_map, args=(map, "matrix", False))
    job_for_another_core.start()
  
  elif option == "2":
    job_for_another_core = multiprocessing.Process(target=draw_map, args=(map, "real", False))
    job_for_another_core.start()
  
  elif option == "3":
    city_id = input("\nCity ID: ")

    try:
      city = map.get_city_by_id(city_id)

      if city == None:
        print("\nCity not found")

      else:
        print("\n")
        print_dict(city)

    except Exception as e:
      print(f"\nError: {e}")

    press_to_continue()
  
  elif option == "4":
    city_id_1 = input("\nCity ID 1: ")
    city_id_2 = input("City ID 2: ")

    try:
      routes = map.get_routes_between_cities(city_id_1, city_id_2)

      print("\n")
      print_dict(routes)

    except Exception as e:
      print(f"\nError: {e}")

    press_to_continue()
  
  elif option == "5":
    city_id = input("\nDestination City ID: ")

    try:
      depth_first_search(map, city_id)

    except Exception as e:
      print(f"\nError: {e}")

    press_to_continue()
  
  elif option == "6":
    print(map.get_city_by_id(0))
    print(map.get_city_by_id(19))
    # print(map.get_all_cities())
    print(map.get_routes_between_cities(0, 1))

    route = [Car(map, 0, 1)]
    print(sum_vehicles_cost(route))

    press_to_continue() 
  
def clear():
  if 'TERM' not in environ:
    print('\n' * 100)
    return

  if name == 'nt': # windows
    _ = system('cls')
  else: # unix
    _ = system('clear')

def press_to_continue():
  input("\nPress Enter to continue...")

def print_dict(dict):
  print(json_dumps(dict, indent=2))
