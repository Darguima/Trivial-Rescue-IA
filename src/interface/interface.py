from os import system, name, environ
import multiprocessing

from map.map import Map
from map.draw_map import draw_map

from utils.print_utils import *

from algorithms.DFS import depth_first_search
from algorithms.BFS import breadth_first_search
from algorithms.A_star import A_star
from algorithms.greedy import greedy
from algorithms.Dijkstra import dijkstra
from algorithms.bidirectional_bfs import bidirectional_bfs
from algorithms.bidirectional_dfs import bidirectional_dfs
from algorithms.depth_limited_search import depth_limited_search
from algorithms.iddfs import iddfs


def interface(map: Map):
    clear()
    print_centered(
        "==================================================================="
    )
    print_centered(
        "|  _____     _       _       _   ____                             |"
    )
    print_centered(
        "| |_   _| __(_)_   _(_) __ _| | |  _ \\ ___  ___  ___ _   _  ___   |"
    )
    print_centered(
        "|   | || '__| \\ \\ / / |/ _` | | | |_) / _ \\/ __|/ __| | | |/ _ \\  |"
    )
    print_centered(
        "|   | || |  | |\\ V /| | (_| | | |  _ <  __/\\__ \\ (__| |_| |  __/  |"
    )
    print_centered(
        "|   |_||_|  |_| \\_/ |_|\\__,_|_| |_| \\_\\___||___/\\___|\\__,_|\\___|  |"
    )
    print_centered(
        "|                                                                 |"
    )
    print_centered(
        "===================================================================\n"
    )

    print_centered("Select an option:\n")

    print_centered("1. Draw matrix map (land routes)")
    print_centered("2. Draw real map (land routes)")
    print_centered("3. Draw matrix map (sea routes)")
    print_centered("4. Draw matrix map (air routes)")

    print_centered("5. Get Info about city", break_line_before=True)
    print_centered("6. Get capitals cities")
    print_centered("7. Get Info about route")

    print_centered("8. Algorithm Depth First Search", break_line_before=True)
    print_centered("9. Algorithm Breadth First Search")
    print_centered("10. Algorithm A*")
    print_centered("11. Algorithm Greedy (without multiple capitals)")
    print_centered("12. Algorithm IDDFS")
    print_centered("13. Algorithm Dijkstra (without multiple capitals)")
    print_centered("14. Algorithm Bidirectional DFS")
    print_centered("15. Algorithm Bidirectional BFS")
    print_centered("16. Algorithm Depth Limited Search (with multiple capitals)")

    option = input_centered("Option: ", break_line_before=True)
    clear()

    print_centered(f"Option: {option}")
    print_centered(
        "==================================================================="
    )

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
        city_id = input_centered("City ID: ")

        try:
            city = map.get_city_by_id(city_id)

            if city is None:
                print_centered("City not found")
            else:
                print_dict_centered(city)

        except Exception as e:
            print_centered(f"Error: {e}")

        press_to_continue()

    elif option == "6":
        capitals = map.get_capitals()
        print_centered("Capitals IDs:")
        print_dict_centered([capital["id"] for capital in capitals])

        press_to_continue()

    elif option == "7":
        city_id_1 = input_centered("City ID 1: ")
        city_id_2 = input_centered("City ID 2: ")

        try:
            routes = map.get_routes_between_cities(city_id_1, city_id_2)
            print_dict_centered(routes)

        except Exception as e:
            print_centered(f"Error: {e}")

        press_to_continue()

    elif option in {"8", "9", "10", "11", "12", "13", "14", "15", "16"}:
        city_id = input_centered("Destination City ID: ")
        groceries_tons = int(input_centered("Tons of grocery: "))

        # try:
        algorithms = {
            "8": depth_first_search,
            "9": breadth_first_search,
            "10": A_star,
            "11": greedy,
            "12": iddfs,
            "13": dijkstra,
            "14": bidirectional_dfs,
            "15": bidirectional_bfs,
            "16": depth_limited_search,
        }

        path = algorithms[option](map, city_id, groceries_tons)
        do_you_want_draw_the_path(map, path)
        try:
            ...

        except Exception as e:
            print_centered(f"Error: {e}")

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
    input_centered("Press Enter to continue...")


def do_you_want_draw_the_path(map, path):
    if path is None:
        return

    answer = input_centered("Do you want to draw the path? (y/N) ")

    if answer == "y":
        job = multiprocessing.Process(target=draw_map, args=(map, "real", "land", path))
        job.start()
