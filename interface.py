from os import system, name, environ
import multiprocessing

from map import Map
from draw_map import draw_map

def interface(map: Map):
  clear()
  print("=====================================")
  print("            Trivial Rescue           ")
  print("=====================================\n")

  print("Select an option:\n")

  print("1. Draw map")
  print("2. Tests")

  option = input("\nOption: ")

  if option == "1":
    job_for_another_core = multiprocessing.Process(target=draw_map, args=(map,))
    job_for_another_core.start()
  
  elif option == "2":
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