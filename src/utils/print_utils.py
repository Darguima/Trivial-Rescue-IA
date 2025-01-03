from json import dumps as json_dumps
import shutil

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