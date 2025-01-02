from os import system, name, environ
import multiprocessing
from json import dumps as json_dumps
import shutil

from map.map import Map
from map.draw_map import draw_map
from vehicles.car import Car
from vehicles.sum_vehicles_cost import sum_vehicles_cost

from algorithms.DFS import depth_first_search
from algorithms.BFS import breadth_first_search
from algorithms.A_star import A_star
from algorithms.dario import dario
from algorithms.dionisio import dionisio


def print_centered(text=""):
    """Imprime texto centrado no terminal."""
    columns, _ = shutil.get_terminal_size()
    print(text.center(columns))


def input_inline(prompt=""):
    """Exibe um prompt na mesma linha para entrada."""
    print(prompt, end="", flush=True)
    return input()


def input_centered(prompt=""):
    """Imprime um prompt centrado e lê a entrada na mesma linha."""
    columns, _ = shutil.get_terminal_size()
    padding = (columns - len(prompt)) // 2
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

    print_centered("1. Draw matrix map")
    print_centered("2. Draw real map")
    print_centered("3. Get Info about city")
    print_centered("4. Get capitals cities")
    print_centered("5. Get Info about route\n")

    print_centered("6. Algorithm Depth First Search")
    print_centered("7. Algorithm Breadth First Search")
    print_centered("8. Algorithm A*")
    print_centered("9. Algorithm (dionisio, inventa um nome para aqui)")
    print_centered("10. Algorithm (à lá Dário)\n")

    print_centered("0. Code Examples\n")

    option = input_centered("Option: ")
    clear()  # Limpa a tela para centralizar os resultados subsequentes
    print_centered(f"Option: {option}")
    print_centered("===================================================================")

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

    elif option == "4":
        capitals = map.get_capitals()
        print_centered("Capitals IDs:")
        print_dict_centered([capital["id"] for capital in capitals])

        press_to_continue()

    elif option == "5":
        city_id_1 = input_centered("City ID 1: ")
        city_id_2 = input_centered("City ID 2: ")

        try:
            routes = map.get_routes_between_cities(city_id_1, city_id_2)
            print_dict_centered(routes)

        except Exception as e:
            print_centered(f"Error: {e}")

        press_to_continue()

    elif option in {"6", "7", "8", "9", "10"}:
        city_id = input_centered("Destination City ID: ")
        groceries_tons = int(input_centered("Tons of grocery: "))

        try:
            algorithms = {
                "6": depth_first_search,
                "7": breadth_first_search,
                "8": A_star,
                "9": dionisio,
                "10": dario,
            }
            path = algorithms[option](map, city_id, groceries_tons)
            do_you_want_draw_the_path(map, path)

        except Exception as e:
            print_centered(f"Error: {e}")

        press_to_continue()

    elif option == "0":
        print_dict_centered(map.get_city_by_id(0))
        print_dict_centered(map.get_capitals())
        print_dict_centered(map.get_routes_between_cities(0, 1))

        route = [Car(map, 0, 1)]
        print_centered(str(sum_vehicles_cost(route)))

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

    if answer.lower() == "y":
        job = multiprocessing.Process(target=draw_map, args=(map, "real", path))
        job.start()
