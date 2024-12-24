from typing import Tuple


def distance_between_coords(coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
    """
    Calculate the distance between two coordinates.
    Be careful to use the real coordinates, not the ones in the matrix.
    """

    distance = ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    return distance
