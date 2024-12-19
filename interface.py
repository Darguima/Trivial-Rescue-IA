from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps

from map import Map
from draw_map import draw_map

def interface(map: Map):
  clear()
  print("=====================================")
  print("            Trivial Rescue           ")
  print("=====================================\n")

  print("Select an option:\n")

  print("1. Draw map")
  print("2. Get Info about city")
  print("3. Get Info about route")
  print("4. Tests")

  option = input("\nOption: ")

  if option == "1":
    job_for_another_core = multiprocessing.Process(target=draw_map, args=(map,))
    job_for_another_core.start()
  
  elif option == "2":
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
  
  elif option == "3":
    city_id_1 = input("\nCity ID 1: ")
    city_id_2 = input("City ID 2: ")

    try:
      routes = map.get_routes_between_cities(city_id_1, city_id_2)

      print("\n")
      print_dict(routes)

    except Exception as e:
      print(f"\nError: {e}")

    press_to_continue()
  
  elif option == "4":
    print(map.get_city_by_id(0))
    print(map.get_city_by_id(19))
    # print(map.get_all_cities())
    print(map.get_routes_between_cities(0, 1))
    print(map.get_routes_between_cities(19, 20))

    # route = [Car(map, 11, 7), Car(map, 7, 2), Truck(map, 2, 1), Truck(map, 1, 0)]
    # print(sum_vehicles_cost(route))

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
