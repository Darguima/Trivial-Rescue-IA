from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps

from map.map import Map
from map.draw_map import draw_map

from algorithms.DFS import depth_first_search
from algorithms.BFS import breadth_first_search
from algorithms.A_star import A_star
from algorithms.greedy import greedy
from algorithms.dario import dario
from algorithms.Dijkstra import dijkstra
from algorithms.bidirectional_bfs import bidirectional_bfs
from algorithms.bidirectional_dfs import bidirectional_dfs


def interface(map: Map):
    clear()
    print("=====================================")
    print("            Trivial Rescue           ")
    print("=====================================\n")

    print("Select an option:\n")

    print("1. Draw matrix map (land routes)")
    print("2. Draw real map (land routes)")
    print("3. Draw matrix map (sea routes)")
    print("4. Draw matrix map (air routes)")

    print("\n5. Get Info about city")
    print("6. Get capitals cities")
    print("7. Get Info about route")
    
    print("\n8. Algorithm Depth First Search")
    print("9. Algorithm Breadth First Search")
    print("10. Algorithm A*")
    print("11. Algorithm Greedy")
    print("12. Algorithm (à lá Dário)")
    print("13. Algorithm Dijkstra")
    print("14. Algorithm Bidirectional")

    option = input("\nOption: ")

    if option == "1":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "matrix", "land")
        )
        job_for_another_core.start()

    elif option == "2":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "real", "land")
        )
        job_for_another_core.start()
    
    if option == "3":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "matrix", "sea")
        )
        job_for_another_core.start()

    elif option == "4":
        job_for_another_core = multiprocessing.Process(
            target=draw_map, args=(map, "matrix", "air")
        )
        job_for_another_core.start()

    elif option == "5":
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

    elif option == "6":
        capitals = map.get_capitals()

        print("\nCapitals IDs:")
        print_dict([capital["id"] for capital in capitals])

        press_to_continue()

    elif option == "7":
        city_id_1 = input("\nCity ID 1: ")
        city_id_2 = input("City ID 2: ")

        try:
            routes = map.get_routes_between_cities(city_id_1, city_id_2)

            print("\n")
            print_dict(routes)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "8":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        try:
            path = depth_first_search(map, city_id, groceries_tons)

            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "9":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))
 
        try:
            path = breadth_first_search(map, city_id, groceries_tons)
            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "10":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        try:
            path = A_star(map, city_id, groceries_tons)
            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "11":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        try:
            path = greedy(map, city_id, groceries_tons)
            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print(f"\nError: {e}")

        press_to_continue()

    elif option == "12":
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

    elif option == "13":
        city_id = input("\nDestination City ID: ")
        groceries_tons = int(input("\nTons of grocery: "))

        path = dijkstra(map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            # dario(map, city_id, groceries
            ...
        except Exception as e:
            print(f"\nError: {e}")
        press_to_continue()

    elif option == "14":
    # Ask for the type of search: BFS or DFS
        search_type = input("\nChoose search type: 1) BFS or 2) DFS: ")

        if search_type == "1":
            city_id = input("\nDestination City ID: ")
            groceries_tons = int(input("\nTons of groceries: "))

            # Call bidirectional BFS
            path = bidirectional_bfs(map, city_id, groceries_tons)
            if path:
                do_you_want_draw_the_path(map, path)  # Draw the path if found
            else:
                print("\nNo path found using BFS.")
        
        elif search_type == "2":
            city_id = input("\nDestination City ID: ")
            groceries_tons = int(input("\nTons of groceries: "))

            # Call bidirectional DFS
            path = bidirectional_dfs(map, city_id, groceries_tons)
            if path:
                do_you_want_draw_the_path(map, path)  # Draw the path if found
            else:
                print("\nNo path found using DFS.")

        try:
            # Handle additional actions or functions if needed (currently commented out)
            # dario(map, city_id, groceries)
            pass
        except Exception as e:
            print(f"\nError: {e}")

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
        job = multiprocessing.Process(target=draw_map, args=(map, "real", "land", path))
        job.start()
    else:
        pass
    return
