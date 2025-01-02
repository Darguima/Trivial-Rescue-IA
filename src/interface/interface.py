from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps

from map.map import Map
from map.draw_map import draw_map
from vehicles.car import Car
from vehicles.sum_vehicles_cost import sum_vehicles_cost

from algorithms.DFS import depth_first_search
from algorithms.BFS import breadth_first_search
from algorithms.A_star import A_star
from algorithms.dario import dario
from algorithms.dionisio import dionisio


def interface(map: Map):
    clear()
    print("=====================================")
    print("            Trivial Rescue           ")
    print("=====================================\n")

    print("Select an option:\n")

    print("1. Draw matrix map")
    print("2. Draw real map")
    print("3. Get Info about city")
    print("4. Get capitals cities")
    print("5. Get Info about route")

    print("\n6. Algorithm Depth First Search")
    print("7. Algorithm Breadth First Search")
    print("8. Algorithm A*")
    print("9. Algorithm (dionisio, inventa um nome para aqui)")
    print("10. Algorithm (à lá Dário)")

    print("\n0. Code Examples")

    option = input("\nOption: ")

    if option == "1":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "matrix")
        )
        job_for_another_core.start()

    elif option == "2":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "real")
        )
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
        capitals = map.get_capitals()

        print("\nCapitals IDs:")
        print_dict([capital["id"] for capital in capitals])

        press_to_continue()

    elif option == "5":
        city_id_1 = input("\nCity ID 1: ")
        city_id_2 = input("City ID 2: ")

        try:
            routes = map.get_routes_between_cities(city_id_1, city_id_2)

            print("\n")
            print_dict(routes)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "6":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        try:
            path = depth_first_search(map, city_id, groceries_tons)

            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "7":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        path = breadth_first_search(map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            ...

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "8":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        path = A_star(map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            ...
            

           

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "9":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        path = dionisio(map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            # dionisio(map, city_id, groceries_tons)
            ...

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "10":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        path = dario(map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            # dario(map, city_id, groceries_tons)
            ...

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "0":
        print(map.get_city_by_id(0))
        print(map.get_capitals())
        # print(map.get_all_cities())
        print(map.get_routes_between_cities(0, 1))

        route = [Car(map, 0, 1)]
        print(sum_vehicles_cost(route))

        press_to_continue()


def clear():
    if "TERM" not in environ:
        print("\n" * 100)
        return

    if name == "nt":  # windows
        _ = system("cls")
    else:  # unix
        _ = system("clear")


def press_to_continue():
    input("\nPress Enter to continue...")


def print_dict(dict):
    print(json_dumps(dict, indent=2))


def do_you_want_draw_the_path(map, path):
    if path is None:
        return

    answer = input("\nDo you want to draw the path? (y/N) ")

    if answer == "y":
        job = multiprocessing.Process(target=draw_map, args=(map, "real", path))
        job.start()
    else:
        pass
    return
