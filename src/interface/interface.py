from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps
import shutil

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


def print_centered(text="", break_line_before=False):
    """Imprime texto centrado no terminal."""
    columns, _ = shutil.get_terminal_size()
    if break_line_before:
        print("\n")
    print(text.center(columns))


def input_inline(prompt=""):
    """Exibe um prompt na mesma linha para entrada."""
    print(prompt, end="", flush=True)
    return input()


def input_centered(prompt="", break_line_before=False):
    """Imprime um prompt centrado e lê a entrada na mesma linha."""
    columns, _ = shutil.get_terminal_size()
    padding = (columns - len(prompt)) // 2

    if break_line_before:
        print("\n")

    print(" " * padding + prompt, end="", flush=True)
    return input()


def print_dict_centered(dict_obj):
    """Imprime um dicionário formatado e centrado."""
    json_output = json_dumps(dict_obj, indent=2)
    for line in json_output.splitlines():
        print_centered(line)


def interface(map: Map):
    clear()
    print_centered("===================================================================")
    print_centered("|  _____     _       _       _   ____                             |")
    print_centered("| |_   _| __(_)_   _(_) __ _| | |  _ \\ ___  ___  ___ _   _  ___   |")
    print_centered("|   | || '__| \\ \\ / / |/ _` | | | |_) / _ \\/ __|/ __| | | |/ _ \\  |")
    print_centered("|   | || |  | |\\ V /| | (_| | | |  _ <  __/\\__ \\ (__| |_| |  __/  |")
    print_centered("|   |_||_|  |_| \\_/ |_|\\__,_|_| |_| \\_\\___||___/\\___|\\__,_|\\___|  |")
    print_centered("|                                                                 |")
    print_centered("===================================================================\n")

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
    print_centered("11. Algorithm Greedy")
    print_centered("12. Algorithm (à lá Dário)")
    print_centered("13. Algorithm Dijkstra")
    print_centered("14. Algorithm Bidirectional DFS")
    print_centered("15. Algorithm Bidirectional BFS")

    option = input_centered("Option: ", break_line_before=True)
    clear()

    print_centered(f"Option: {option}")
    print_centered("===================================================================")

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
        city_id = input_centered("\nCity ID: ")

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
        city_id_1 = input_centered("\nCity ID 1: ")
        city_id_2 = input_centered("City ID 2: ")

        try:
            routes = map.get_routes_between_cities(city_id_1, city_id_2)
            print_dict_centered(routes)

        except Exception as e:
            print_centered(f"Error: {e}")

        press_to_continue()

    elif option in {"8", "9", "10", "11", "12", "13", "14", "15"}:
        city_id = input_centered("Destination City ID: ")
        groceries_tons = int(input_centered("Tons of grocery: "))
        
        try:
            algorithms = {
                "8": depth_first_search,
                "9": breadth_first_search,
                "10": A_star,
                "11": greedy,
                "12": dario,
                "13": dijkstra,
                "14": bidirectional_dfs,
                "15": bidirectional_bfs,
            }
            path = algorithms[option](map, city_id, groceries_tons)
            do_you_want_draw_the_path(map, path)

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
